# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Package.deployed_at'
        db.add_column(u'packages_package', 'deployed_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=None, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Package.deployed_at'
        db.delete_column(u'packages_package', 'deployed_at')


    models = {
        u'packages.package': {
            'Meta': {'object_name': 'Package'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deployed_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'projects.filesystem': {
            'Meta': {'object_name': 'FileSystem'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mount_point': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2000'})
        },
        u'projects.project': {
            'Meta': {'unique_together': "(('file_system', 'directory'),)", 'object_name': 'Project'},
            'directory': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'file_system': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.FileSystem']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['packages']