from django.urls import path
from core import views

# Avoid namespace collision with url
app_name = 'core'

urlpatterns = [
    # resource views
    path('<slug:type_slug>/', views.resource_list, name='resource_list'),
    path('<slug:type_slug>/<slug:resource_slug>/',
         views.resource_detail,
         name='resource_detail'),
]
