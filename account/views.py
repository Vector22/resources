from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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
