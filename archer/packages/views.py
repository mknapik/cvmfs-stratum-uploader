from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from guardian.decorators import permission_required_or_403
from django.core.exceptions import PermissionDenied
from guardian.shortcuts import get_objects_for_user

from archer.projects.models import Project
from archer.packages.models import Package


def show(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    project = get_object_or_404(Project, id=package.project_id)
    if not request.user.has_perm('projects.view_project', project):
        raise PermissionDenied

    can_deploy = request.user.has_perm('packages.deploy_package', package) \
        and request.user.has_perm('projects.deploy_package', project)
    can_remove = request.user.has_perm('packages.remove_package', package)
    return render(request, 'packages/show.html', {
        'package': package,
        'files': package.get_file_list(),
        'can_deploy': can_deploy,
        'can_remove': can_remove,})


@permission_required_or_403('packages.deploy_package', (Package, 'pk', 'package_id'))
def deploy(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    project = Project.objects.get(pk=package.project_id)
    if not request.user.has_perm('projects.deploy_package', project):
        raise PermissionDenied
    if not package.can_deploy():
        messages.add_message(request, messages.ERROR, 'Cannot deploy a package!')
        return render(request, 'packages/show.html', {'package': package})
    else:
        # for p in Package.objects.filter(status=Package.Status.deployed):
        #     p.undeploy()
        try:
            if request.POST.has_key('subdir'):
                result = package.deploy(request.POST['subdir'])
            else:
                result = package.deploy()
            if result:
                messages.add_message(request, messages.INFO, 'Package deployed!')
            else:
                messages.add_message(request, messages.ERROR, 'Error during deployment of the package.')
        except IOError as e:
            messages.add_message(request, messages.ERROR, 'Error during deployment of the package: ' + str(e))

        return render(request, 'packages/show.html', {'package': package})


@permission_required_or_403('packages.remove_package', (Package, 'pk', 'package_id'))
def clear(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    project_id = package.project_id

    if package.can_clear():
        package.remove()
        package.delete()
        messages.add_message(request, messages.SUCCESS, 'Package was completely removed!')
    else:
        messages.add_message(request, messages.ERROR, 'Cannot delete package file!')
        return render(request, 'packages/show.html', {'package': package, 'can_remove': True})
    return HttpResponseRedirect(reverse('projects:show', args=[project_id]))


@permission_required_or_403('packages.remove_package', (Package, 'pk', 'package_id'))
def remove(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if package.can_remove():
        try:
            if package.remove():
                messages.add_message(request, messages.INFO, 'Package file successfully deleted!')
            else:
                messages.add_message(request, messages.WARNING,
                                     'Package file was already deleted from the file system. Mark as deleted.')
        except IOError as e:
            messages.add_message(request, messages.ERROR, e)
    else:
        messages.add_message(request, messages.ERROR, 'Cannot delete package file!')
    return HttpResponseRedirect(reverse('packages:show', args=[package.id]))
