"""resources URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from core.views import resource_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    # We want to display the list of resource in the URL http://127.0.0.1:8000/
    # and all other URLs for the core app have the /core/resource/ prefix.
    path('', resource_list, name='home'),
    path('core/resource/', include('core.urls')),
]

if settings.DEBUG:
    # We serve media files only on development mode
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
