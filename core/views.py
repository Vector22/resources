from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

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

                messages.success(request,
                                 _("Successfuly submit a reservation."))
            else:
                error_text = _("This resource is not free at this time. ")
                error_text += _("Please try with another date or time.")
                messages.error(request, error_text)
        else:
            messages.error(request,
                           _("Try to correct these errors and try again."))
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


@login_required
def reservation_list(request):
    user = request.user

    if user.is_staff:
        # Retrieve all reservations and group them by resource
        # The admin users see all the reservations
        res_by_resource = [
            Reservation.objects.filter(resource__slug=resource.slug)
            for resource in Resource.available.all()
        ]
    else:
        # The non admin user see only its own reservartions
        res_by_resource = [
            Reservation.objects.filter(resource__slug=resource.slug).filter(
                user_id=user.id) for resource in Resource.available.all()
        ]

    context = {
        'res_by_resource': res_by_resource,
    }

    return render(request, 'core/reservation_list.html', context)


@login_required
def reservation_detail(request, resource_slug, pk):
    resource = get_object_or_404(Resource, slug=resource_slug)
    reservation = get_object_or_404(Reservation, id=pk)

    context = {
        'resource': resource,
        'reservation': reservation,
    }

    return render(request, 'core/reservation_detail.html', context)


# Let use CBV for update/detail and delete reservation
class ReservationUpdateView(LoginRequiredMixin, UpdateView):

    model = Reservation
    fields = ['title', 'overview', 'start_date', 'end_date']

    template_name = 'core/reservation_detail.html'
    context_object_name = 'reserv'

    def get_success_url(self):
        return reverse_lazy('core:reserv_detail',
                            kwargs={
                                'resource_slug': self.object.resource.slug,
                                'pk': self.object.id,
                            })

    def get(self, request, *args, **kwargs):
        self.obj = get_object_or_404(Reservation, id=self.kwargs.get('pk'))
        self.resource = get_object_or_404(
            Resource, slug=self.kwargs.get('resource_slug'))

        # Try to increase the number of the form textarea row but don't work
        ReservationModelForm.base_fields['overview'].widget.attrs['rows'] = '3'

        self.form = ReservationModelForm(instance=self.obj,
                                         initial={
                                             'start_date': self.obj.start_date,
                                             'end_date': self.obj.end_date,
                                         })
        return render(request, self.template_name, {
            "reserv": self.obj,
            "form": self.form,
            "resource": self.resource
        })


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'core/reservation_delete.html'
    context_object_name = 'reserv'

    def get_success_url(self):
        return reverse_lazy('core:rserv_list')