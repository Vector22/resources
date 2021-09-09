from django.shortcuts import render, get_object_or_404
from .models import Resource


def resource_list(request, type_slug=None):
    """
        This view is handled by two differents urls
        the 'home' (defined in project url level) and
        the 'resource_list' (defied in core app urls).
    """
    resources = Resource.available.all()

    if type_slug:
        resources = resources.filter(type__slug=type_slug)
    context = {
        'resources': resources,
    }
    return render(request, 'core/resource/list.html', context)


def resource_detail(request, type_slug, resource_slug):
    resource = get_object_or_404(Resource,
                                 type_slug=type_slug,
                                 resource_slug=resource_slug)
    context = {
        'resource': resource,
    }
    return render(request, 'core/resource/detail.html', context)
