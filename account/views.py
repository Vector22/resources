from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.timezone import get_current_timezone_name

from account.models import Profile


@login_required
def dashboard(request):
    user = request.user
    context = {
        'user': user,
        'section': 'dashboard',
    }
    return render(request, 'registration/dashboard.html', context)


def register(request):
    context = {
        'section': 'register',
    }
    return render(request, 'registration/register.html', context)


# Use CBV for create new user and provide new user profile
class UserRegistrationView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('account:dashboard')

    def form_valid(self, form):
        # Login the user after valid submission
        result = super(UserRegistrationView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        # Create a profile for this user
        profile = Profile.objects.create(user=user,
                                         time_zone=get_current_timezone_name())
        profile.save()
        # Login the user after regitering with success
        login(self.request, user)
        return result
