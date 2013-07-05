from django.db import models

# Create your models here.

# class User(models.Model):
#     name = models.CharField(max_length=200, null=False)
#     cert = models.CharField(max_length=1000)
#
#     def __unicode__(self):
#         return 'User[name=' + str(self.name) + ', cert=' + str(self.cert) + ']'


class CvmFs(models.Model):
    mount_point = models.CharField(max_length=2000, null=False, blank=False, unique=True)

    def __unicode__(self):
        return self.mount_point


class Package(models.Model):
    STATUSES = [(a, a) for a in ['new', 'uploading', 'uploaded', 'unpacking', 'unpacked', 'cancelled', 'error']]
    STATUSES_LENGTH = 10 # max(STATUSES, key=len)
    fs = models.ForeignKey(CvmFs)
    file_path = models.FilePathField(path='/', allow_files=True, allow_folders=False, null=True)
    file = models.FileField(upload_to='uploads/',)
    status = models.CharField(max_length=STATUSES_LENGTH, choices=STATUSES, blank=False, null=False)

    def __unicode__(self):
        return 'Package[fs=' + str(self.fs) + ', file_path=' + self.file_path + ']'

    class Meta:
        unique_together = ('fs', 'file_path',)


class Tarball(models.Model):
    from multiuploader.forms import MultiuploaderField

    name = models.CharField(max_length=2000, null=False, blank=False, unique=True)
    files = MultiuploaderField(required=False)

    def __unicode__(self):
        return str(self.name) + ' ' + str(self.files)