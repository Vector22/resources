from django.urls import path
from django.views.decorators.cache import cache_page
from core import views

# Avoid namespace collision with url
app_name = 'core'

urlpatterns = [
    # Reservation views
    path('reservation/', views.reservation_list, name='reserv_list'),
    path('reservation_delete/<int:pk>/',
         views.ReservationDeleteView.as_view(),
         name='reserv_delete'),
    path('<slug:resource_slug>/reservation/<int:pk>/',
         cache_page(60 * 15)(views.ReservationUpdateView.as_view()),
         name='reserv_detail'),
    # Resources views
    path('<slug:type_slug>/', views.resource_list, name='resource_list'),
    path('<slug:type_slug>/<slug:resource_slug>/',
         cache_page(60 * 15)(views.resource_detail),
         name='resource_detail'),
]

# Note: We cached the resource and reservation detail page for 15 minutes
