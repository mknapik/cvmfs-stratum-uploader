import re
import shutil
import os
import tarfile

from django.db import models
from django.conf import settings
from archer.projects.models import Project


class Package(models.Model):
    def __get_upload_path(instance, filename):
        return os.path.join(settings.MEDIA_ROOT, ".%s" % instance.project, filename).replace('/./', '/')

    class Status:
        new, uploaded, unpacking, deployed, cancelled, deleted, undeployed, error = range(8)

    __STATUSES = dict((value, name) for name, value in vars(Status).items() if not name.startswith('__'))

    project = models.ForeignKey(Project)
    file = models.FileField(upload_to=__get_upload_path, max_length=1024)
    status = models.IntegerField(
        choices=__STATUSES.items(),
        blank=False,
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ('deploy_package', 'Deploy package'),
            ('remove_package', 'Remove package'),
        )

    def status_name(self):
        return Package.__STATUSES[self.status]

    def can_remove(self):
        return self.status in [Package.Status.deployed, Package.Status.undeployed, Package.Status.uploaded]

    def can_deploy(self):
        return self.status in [Package.Status.uploaded, Package.Status.undeployed, Package.Status.cancelled] \
            and (os.path.isfile(self.file.path) and tarfile.is_tarfile(self.file.path))

    def filepath(self):
        return self.file.path.replace(settings.MEDIA_ROOT, '')

    def filename(self):
        return self.file.path.replace(os.path.join(settings.MEDIA_ROOT, self.project.full_path()[1::]) + '/', '')

    @staticmethod
    def clear_dir(dir):
        try:
            for root, dirs, files in os.walk(dir):
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
            return True
        except IOError as e:
            print e
            return False

    def get_file_list(self):
        path = self.file.path
        if not os.path.isfile(path):
            return None
        if not tarfile.is_tarfile(path):
            return None
        tar = tarfile.open(path)
        names = tar.getnames()
        return names

    def deploy(self, force=False):
        import tarfile

        if self.can_deploy or force:
            path = self.file.path
            if not os.path.isfile(path):
                raise IOError('package file ' + path + ' does not exist')
            self.status = Package.Status.unpacking
            self.save()
            if not tarfile.is_tarfile(path):
                self.status = Package.Status.error
                self.save()
                raise IOError('package file ' + path + ' is not tarball file')
            cleared = Package.clear_dir(self.project.full_path())
            if cleared:
                tar = tarfile.open(path)
                # tar.list()
                tar.extractall(path=self.project.full_path())
                tar.close()
                self.status = Package.Status.deployed
                self.save()
                return True
            else:
                self.status = Package.Status.error
                self.save()
                return False
        else:
            return False

    def remove(self):
        result = False
        if os.path.isfile(self.file.path):
            os.unlink(self.file.path)
            result = True
        self.status = Package.Status.deleted
        self.save()
        return result

    def __unicode__(self):
        return 'Package[project=' + str(self.project) + ', file=' + str(self.file) + ', status=' + Package.__STATUSES[
            self.status] + ']'