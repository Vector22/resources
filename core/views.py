from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from core.models import Reservation, Resource
from core.forms import ReservationModelForm
from core.utils import overlap


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
    if request.method == 'POST':
        form = ReservationModelForm(request.POST)
        if form.is_valid():
            # We need to provide some required datas, then use 'commit=False'
            reservation = form.save(commit=False)
            # Here we check if the ressource is free at the requested time
            reservations = Reservation.objects.filter(resource=resource)
            is_overlaped = 0
            if reservations:
                date_start = form.cleaned_data['start_date']
                date_end = form.cleaned_data['end_date']
                res_range = []
                for res in reservations:
                    temp_range = {'start': res.start_date, 'end': res.end_date}
                    res_range.append(temp_range)

                for date in res_range:
                    # Check the user date range with the existing reservation
                    # date range. If one is overlaped then the user can't
                    # choose this date range for reservation
                    date_overlap = overlap(date_start, date_end, date['start'],
                                           date['end'])
                    if date_overlap:
                        is_overlaped = date_overlap
                        break

            if not is_overlaped:
                reservation.status = 'pending'
                reservation.user = request.user
                reservation.resource = resource
                # Now we can save the form
                reservation.save()

                messages.success(request, "Successfuly submit a reservation.")
            else:
                error_text = "This resource is not free at this time. "
                error_text += "Please try with another date or time."
                messages.error(request, error_text)
        else:
            messages.error(request,
                           "Try to correct these errors and try again.")
        return redirect('core:resource_detail', type_slug, resource_slug)
    else:
        reservations = Reservation.objects.filter(resource=resource)
        form = ReservationModelForm()
        context = {
            'form': form,
            'resource': resource,
            'reservations': reservations,
        }
        return render(request, 'core/resource_detail.html', context)
