from django.urls import path
from rest_framework import permissions
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt import views as jwt_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.views import (ResourceViewSet, ResourceTypeList, ResourceTypeDetail,
                       ResourceGalleryList, ResourceGalleryDetail,
                       ReservationViewSet)

# Documentation purposes
schema_view = get_schema_view(
    openapi.Info(
        title="Resource API",
        default_version="v1",
        description="A sample API for resource with DRF",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="rekinvector@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(
        permissions.AllowAny, ),  # Anyone have access to API documentation
)

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

    # Django all auth | Not able to use because of namespace conflict
    # with the custom account application
    # path('api/v1/auth/', include('dj_rest_auth.urls')),  # Login Logout ...
    # path('api/v1/registration/', include('dj_rest_auth.registration.urls')),

    # Add schemas and documentation urls
    path(
        'doc/',  # We use swagger here
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    path(
        'redoc/',  # Here is redoc like documentation
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]

# Routers for viewsets
router = SimpleRouter()
router.register('reservations', ReservationViewSet, basename='reservations')
router.register('', ResourceViewSet, basename='resources')

urlpatterns += router.urls
