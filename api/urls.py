from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt import views as jwt_views
from api.views import (ResourceViewSet, ResourceTypeList, ResourceTypeDetail,
                       ResourceGalleryList, ResourceGalleryDetail,
                       ReservationViewSet)

urlpatterns = [
    # ResourceType urls
    path('resource_type/<int:pk>/', ResourceTypeDetail.as_view()),
    path('resource_type/', ResourceTypeList.as_view()),
    # Resource urls
    # path('<int:pk>/', ResourceDetail.as_view()),
    # path('', ResourceList.as_view()),
    # Resource Gallery urls
    path('resource_gallery/<int:pk>/', ResourceGalleryDetail.as_view()),
    path('resource_gallery/', ResourceGalleryList.as_view()),
    # Reservation urls
    # path('reservation/<int:pk>/', ReservationDetail.as_view()),
    # path('reservation/', ReservationList.as_view()),

    # Api authorization
    path('token/',
         jwt_views.TokenObtainPairView.as_view(),
         name='get_auth_token'),
    path('token/refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name='refresh_token'),
]

# Routers for viewsets
router = SimpleRouter()
router.register('reservations', ReservationViewSet, basename='reservations')
router.register('', ResourceViewSet, basename='resources')

urlpatterns += router.urls
