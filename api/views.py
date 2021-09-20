from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from core.models import Resource, ResourceType, ResourceGallery, Reservation
from api.serializers import (ResourceSerializer, ResourceTypeSerializer,
                             ResourceGallerySerializer, ReservationSerializer)

# Here i use both viewsets and generics as base view
# viewsets because some times, it's less code to writte.
# But in general i prefer generics views, because it keeps things simple


# Resource type views
class ResourceTypeList(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    queryset = ResourceType.objects.all()

    serializer_class = ResourceTypeSerializer

    # Handle the picture upload
    def post(self, request, format=None):
        serializer = ResourceTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ResourceTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser, FormParser]
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer

    # Handle the picture upload
    def post(self, request, format=None):
        serializer = ResourceTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


# Resource gallery views
class ResourceGalleryList(generics.ListCreateAPIView):
    queryset = ResourceGallery.objects.all()
    serializer_class = ResourceGallerySerializer


class ResourceGalleryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ResourceGallery.objects.all()
    serializer_class = ResourceGallerySerializer


# Resource views
# class ResourceList(generics.ListCreateAPIView):
#     queryset = Resource.objects.all()
#     serializer_class = ResourceSerializer

# class ResourceDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Resource.objects.all()
#     serializer_class = ResourceSerializer


# Use viewsets for resource object model
class ResourceViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ResourceSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned resources to a given type,
        by filtering against a `type` query parameter in the URL.
        """
        queryset = Resource.objects.all()

        # Filter the resources by type, city, country
        type = self.request.query_params.get('type')
        city = self.request.query_params.get('city')
        country = self.request.query_params.get('country')
        if type is not None:
            queryset = queryset.filter(type__name__icontains=type)
        if city is not None:
            queryset = queryset.filter(city__icontains=city)
        if country is not None:
            queryset = queryset.filter(country__icontains=country)
        return queryset

    # Handle the picture upload
    def post(self, request, format=None):
        serializer = ResourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


# Reservation views
# class ReservationList(generics.ListCreateAPIView):
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer

# class ReservationDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer


# Use viewsets for reservation object model
class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned reservation to a given date
        or/and given hour by filtering against a `date` or/and `hour`
        query parameter in the URL.
        """
        queryset = Reservation.objects.all()

        # Filter the reservations by day or/and hour
        date_day = self.request.query_params.get('date_day')
        date_hour = self.request.query_params.get('date_hour')

        # Filter the reservations by resource name (icontains) and by Id
        resource_name = self.request.query_params.get('resource_name')
        resource_id = self.request.query_params.get('resource_id')

        # Filter the reservations by username or/and user id
        username = self.request.query_params.get('username')
        user_id = self.request.query_params.get('user_id')

        if date_day is not None:
            queryset = queryset.filter(start_date__day=date_day)
        if date_hour is not None:
            queryset = queryset.filter(start_date__hour=date_hour)
        if resource_id is not None:
            queryset = queryset.filter(resource__id=resource_id)
        if resource_name is not None:
            queryset = queryset.filter(resource__name=resource_name)
        if user_id is not None:
            queryset = queryset.filter(user__id=user_id)
        if username is not None:
            queryset = queryset.filter(user__username=username)

        return queryset
