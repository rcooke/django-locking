Concurrency control with django-locking
=======================================

Django has seen great adoption in the content management sphere, especially among the newspaper crowd. One of the trickier things to get right, is to make sure that nobody steps on each others toes while editing and modifying existing content. Newspaper editors might not always be aware of what other editors are up to, and this goes double for distributed teams. When different people work on the same content, the one who saves last will win the day, while the other edits are overwritten.

`django-locking` provides a system that makes concurrent editing impossible, and informs users of what other users are working on and for how long that content will remain locked. Users can still read locked content, but cannot modify or save it.

``django-locking`` makes sure no two users can edit the same content at the same time, preventing annoying overwrites and lost time. Find the repository and download the code at http://github.com/stdbrouw/django-locking

This version of ``django-locking`` is intended to work with Python 3.6 and Django 2.0 and probably shouldn't be relied on without reading the code and commit comments, then having a good sit down with a cup of tea and a hard think.

Credit
------

This code is basically a composition of the following repos with a taste of detailed descretion from me. Credit goes out to the following authors and repos for their contributions:

 - https://github.com/stdbrouw/django-locking
 - https://github.com/runekaagaard/django-locking
 - https://github.com/theatlantic/django-locking
 - https://github.com/ortsed/django-locking

Major features
==============

Changes on change list pages
----------------------------

Unlock content object from change list page by simply clicking on the lock icon
_______________________________________________________________________________

![unlock prompt](https://github.com/RobCombs/django-locking/raw/master/docs/screenshots/unlock_prompt.png)

Hover over the lock icon to see when the lock expires
_____________________________________________________

![expire status](https://github.com/RobCombs/django-locking/raw/master/docs/screenshots/expire_status.png)

Hover over the username by the lock icon to see the full name of the person who has locked the content object
_____________________________________________________________________________________________________________

![lock_by_who](https://github.com/RobCombs/django-locking/raw/master/docs/screenshots/lock_by_who.png)


Consolidated username and lock icon into one column on change list page

Changes in settings:
----------------------------

Added Lock warning and expiration flags in terms of seconds

Lock messages:
----------------------------

Added options to reload or save the object when lock expiration message is shown

![reload or bust](https://github.com/RobCombs/django-locking/raw/master/docs/screenshots/reload_or_bust.png)

Improved look and feel for the lock messages
Lock messages fade in and out seamlessly
Added much more detail to let users know who the content object was locked by providing the username, first name and last name
Added lock expiration warnings
Shows how much longer the object is locked for in minutes

Locking:
----------------------------

 Added hard locking support using Django's validation framework

![hard lock](https://github.com/RobCombs/django-locking/raw/master/docs/screenshots/hard_lock.png)

 Set hard and soft locking as the default to ensure the integrity of locking
 Added seamless unlocking when lock expires

![auto unlock](https://github.com/RobCombs/django-locking/raw/master/docs/screenshots/auto_unlock.png)


Architecture:
----------------------------

1 model tracks lock information and that's it!  No messy migrations for each model that needs locking.
Refactored and cleaned up code for easier maintainability
 Simplified installation by coupling common functionality into base admin/form/model classes


5 Minute Install
----------------

1) Install:

    pip install git+https://github.com/rcooke/django-locking.git#egg=django-locking

2) Add locking to the list of INSTALLED_APPS in project settings file; you also need `django.contrib.staticfiles` (probably already there):

    INSTALLED_APPS = ('locking', 'django.contrib.staticfiles')

3) Add locking to the admin files that you want locking for:

    from locking.admin import LockableAdmin
    class YourAdmin(LockableAdmin):
       list_display = ('get_lock_for_admin')

4) Add warning and expiration time outs to your Django settings file:

    LOCKING = {'time_until_expiration': 120, 'time_until_warning': 60}

5) Build the Lock table in the database:

    django-admin.py/manage.py migrate locking (For south users. Recommended approach) OR
    django-admin.py/manage.py syncdb (For non south users)

Note that Django's built-in staticfiles cannot serve from an egg, so don't clone from a repo and try to install things that way (unless you create an sdist first). Do the above and you should be fine.

That's it!

Checking the installation
-------------------------
Simulate a lock situation -> Open 2 browsers and hit your admin site with one user logged into the 1st browser and
other user logged into the other.  Go to the model in the admin that you've installed locking for with one browser.
On the other browser, go to the change list/change view pages of the model that you've installed django-locking for.
You'll see locks in the interface similar to the screen shots above.

You can also look at your server console and you'll see the client making ajax calls to the django server checking for locks like so:

    [04/May/2012 15:15:09] "GET /admin/editorial/dispatch/14/locking_variables.js HTTP/1.1" 200 488
    [04/May/2012 15:15:09] "GET /admin/editorial/dispatch/14/lock/?_=1383670147604 HTTP/1.1" 200 200

Optional
--------
If you'd like to enforce hard locking(locking at the database level), then add the LockingForm class to the same admin pages

Example:

    from locking.forms import LockingForm
    class YourAdmin(LockableAdmin):
     list_display = ('get_lock_for_admin')
     form = LockingForm

Note: if you have an existing form and clean method, then call super to invoke the LockingForm's clean method

Example:

    from locking.forms import LockingForm
    class YourFormForm(LockingForm):
      def clean(self):
        self.cleaned_data = super(MedleyRedirectForm, self).clean()
        ...some code
        return self.cleaned_data

Migration dependencies under South
----------------------------------

In order for tests to work you need to ensure that the migration which
creates the ``Lock`` model runs after your user model is created. This
should generally work if you put the ``locking`` app after whatever
app provides the user model (``auth.user`` or your own app if you're
using a custom user model), but if you don't want to do that or it
doesn't work you'll want to add a reverse dependency from the
migration in your app that creates the user model.

For South v1.0 you want to do the following:

    class Migration(SchemaMigration):

        needed_by = (
            ("locking", "0001_initial"),
        )

Django 1.7's migrations system takes care of this for you
automatically.
