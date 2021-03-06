from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from guardian.admin import GuardedModelAdmin
from uploader.projects.models import FileSystem, Project


class FileSystemAdminForm(forms.ModelForm):
    class Meta:
        model = FileSystem


class ProjectAdmin(GuardedModelAdmin):
    list_display = ('__unicode__', 'file_system', 'directory')


class FileSystemAdmin(ModelAdmin):
    list_display = ('__unicode__', 'alias', 'mount_point')
    form = FileSystemAdminForm


admin.site.register(FileSystem, admin_class=FileSystemAdmin)
admin.site.register(Project, admin_class=ProjectAdmin)
