import functools
import json

try:
    from custom_admin import admin
except ImportError:
    from django.contrib import admin

from django import forms
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse
from django.utils import html as html_utils
from django.utils.functional import curry
from django.utils.timesince import timeuntil
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

try:
    from django.template.response import TemplateResponse
except ImportError:
    # django <= 1.2, not fully supported
    class TemplateResponse(object): pass

from .models import Lock
from .forms import locking_form_factory
from . import settings as locking_settings, views as locking_views


json_encode = json.JSONEncoder(indent=4).encode

csrf_protect_m = method_decorator(csrf_protect)


class LockableAdminMixin(object):

    @property
    def media(self):
        return super(LockableAdminMixin, self).media + forms.Media(**{
            'js': (
                static("locking/js/admin.locking.js"),
            ),
            'css': {
                'all': (static('locking/css/locking.css'),),
            }})

    def locking_media(self, obj=None):
        opts = self.model._meta
# https://code.djangoproject.com/ticket/20853
#        info = (opts.app_label, opts.module_name)
        info = (opts.app_label, opts.model_name)
        pk = getattr(obj, 'pk', None) or 0
        return forms.Media(js=(
            reverse('admin:%s_%s_lock_js' % info, args=[pk]),))

    def get_urls(self):
        """
        Appends locking urls to the ModelAdmin's own urls. Its url names
        are patterned after the urls for the ModelAdmin's views (e.g.
        changelist_view, change_view).

        The url names appended are:

            admin:%(app_label)s_%(object_name)s_lock
            admin:%(app_label)s_%(object_name)s_lock_clear
            admin:%(app_label)s_%(object_name)s_lock_remove
            admin:%(app_label)s_%(object_name)s_lock_status
            admin:%(app_label)s_%(object_name)s_lock_js
        """
        from django.conf.urls import patterns, url

        def wrap(view):
            curried_view = curry(view, self)
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(curried_view)(*args, **kwargs)
            return functools.update_wrapper(wrapper, view)

        opts = self.model._meta
# https://code.djangoproject.com/ticket/20853
#        info = (opts.app_label, opts.module_name)
        info = (opts.app_label, opts.model_name)

        urlpatterns = patterns('',
            url(r'^(.+)/locking_variables\.js$',
                wrap(locking_views.locking_js),
                name="%s_%s_lock_js" % info),
            url(r'^(.+)/lock/$',
                wrap(locking_views.lock),
                name="%s_%s_lock" % info),
            url(r'^(.+)/lock_clear/$',
                wrap(locking_views.lock_clear),
                name="%s_%s_lock_clear" % info),
            url(r'^(.+)/lock_remove/$',
                wrap(locking_views.lock_remove),
                name="%s_%s_lock_remove" % info),
            url(r'^(.+)/lock_status/$',
                wrap(locking_views.lock_status),
                name="%s_%s_lock_status" % info))
        urlpatterns += super(LockableAdminMixin, self).get_urls()
        return urlpatterns

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        """
        Append locking media to the changelist view.

        This method will not work properly on django <= 1.2
        """
        response = super(LockableAdminMixin, self).changelist_view(request, extra_context)
        if isinstance(response, TemplateResponse):
            try:
                response.context_data['media'] += self.locking_media()
            except KeyError:
                pass
        return response

    def render_change_form(self, request, context, add=False, obj=None, **kwargs):
        if not add and getattr(obj, 'pk', None):
            locking_media = self.locking_media(obj)
            if isinstance(context['media'], basestring):
                locking_media = unicode(locking_media)
            context['media'] += locking_media
        return super(LockableAdminMixin, self).render_change_form(
                request, context, add=add, obj=obj, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = locking_form_factory(self.model, kwargs.get('form', self.form))
        return super(LockableAdminMixin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, *args, **kwargs):
        """
        Clears the lock owned by the current user, if it wasn't cleared on
        unload, then saves the admin model instance.
        """
        if getattr(obj, 'pk', None):
            try:
                lock = Lock.objects.get_lock_for_object(obj)
            except Lock.DoesNotExist:
                pass
            else:
                if lock.is_locked and lock.is_locked_by(request.user):
                    lock.unlock_for(request.user)
        super(LockableAdminMixin, self).save_model(request, obj, *args, **kwargs)

    def get_queryset(self, request):
        """
        Extended queryset method which adds a custom SQL select column,
        `_locking_user_pk`, which is set to the pk of the current request's
        user instance. Doing this allows us to access the user id by
        obj._locking_user_pk for any object returned from this queryset.
        """
        qs = super(LockableAdminMixin, self).get_queryset(request)
        return qs.extra(select={
            '_locking_user_pk': "%d" % request.user.pk,
        })

    def get_lock_for_admin(self, obj):
        """
        Returns the locking status along with a nice icon for the admin
        interface use in admin list display like so:
        list_display = ['title', 'get_lock_for_admin']
        """
        current_user_id = obj._locking_user_pk

        try:
            lock = Lock.objects.get_lock_for_object(obj)
        except Lock.DoesNotExist:
            return u""
        else:
            if not lock.is_locked:
                return u""

        until = timeuntil(lock.lock_expiration_time)

        locked_by_name = lock.locked_by.get_full_name()
        if locked_by_name:
            locked_by_name = u"%(username)s (%(fullname)s)" % {
                'username': lock.locked_by.get_username(),
                'fullname': locked_by_name,
            }
        else:
            locked_by_name = lock.locked_by.get_username()

        if lock.locked_by.pk == current_user_id:
            msg = _(u"You own this lock for %s longer") %  until
            css_class = 'locking-edit'
        else:
            msg = _(u"Locked by %s for %s longer") % (locked_by_name, until)
            css_class = 'locking-locked'

        return (
            u'  <a href="#" title="%(msg)s"'
            u'     data-locked-obj-id="%(locked_obj_id)s"'
            u'     data-locked-by="%(locked_by_name)s"'
            u'     class="locking-status %(css_class)s"></a>'
        ) % {
            'msg': html_utils.escape(msg),
            'locked_obj_id': obj.pk,
            'locked_by_name': html_utils.escape(locked_by_name),
            'css_class': css_class,}

    get_lock_for_admin.allow_tags = True
    get_lock_for_admin.short_description = 'Lock'


class LockableAdmin(LockableAdminMixin, admin.ModelAdmin):
    pass

# Temporary for Diagnostics: (RCooke)
from .models import Lock

admin.site.register(Lock)

