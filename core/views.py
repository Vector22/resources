from django.shortcuts import render, get_object_or_404
from .models import Reservation, Resource


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
        'news': resources.order_by('created')[:3],
    }
    return render(request, 'core/resource_list.html', context)


def resource_detail(request, type_slug, resource_slug):
    resource = get_object_or_404(Resource,
                                 type__slug=type_slug,
                                 slug=resource_slug)
    reservations = Reservation.objects.filter(resource=resource)
    context = {
        'resource': resource,
        'reservations': reservations,
    }
    return render(request, 'core/resource_detail.html', context)
