# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# With the default User model these will be 'auth.User' and 'auth.user'
# so instead of using orm['auth.User'] we can use orm[user_orm_label]
user_orm_label = '%s.%s' % (User._meta.app_label, User._meta.object_name)
user_model_label = '%s.%s' % (User._meta.app_label, User._meta.module_name)

class Migration(SchemaMigration):
    def forwards(self, orm):
        
        # Adding model 'Lock'
        db.create_table('locking_lock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_locked_at', self.gf('django.db.models.fields.DateTimeField')(null=True, db_column='locked_at')),
            ('app', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('entry_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('_locked_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='working_on_locking_lock', null=True, db_column='locked_by', to=orm[user_orm_label])),
            ('_hard_lock', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='hard_lock', blank=True)),
        ))
        db.send_create_signal('locking', ['Lock'])

    def backwards(self, orm):
        
        # Deleting model 'Lock'
        db.delete_table('locking_lock')

    models = {
        user_model_label: {
            'Meta': {
                'object_name': User.__name__,
                'db_table': "'%s'" % User._meta.db_table
            },
            User._meta.pk.attname: (
                'django.db.models.fields.AutoField', [],
                {'primary_key': 'True',
                'db_column': "'%s'" % User._meta.pk.column}
            ),
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'locking.lock': {
            'Meta': {'object_name': 'Lock'},
            '_hard_lock': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'hard_lock'", 'blank': 'True'}),
            '_locked_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "'locked_at'"}),
            '_locked_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'working_on_locking_lock'", 'null': 'True', 'db_column': "'locked_by'", 'to': "orm['%s']" % user_orm_label}),
            'app': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'entry_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        }
    }
    complete_apps = ['locking']
