from rest_framework import serializers
from core.models import Resource, ResourceType, ResourceGallery, Reservation


class ResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'picture')
        model = ResourceType


class ResourceGallerySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'resource', 'picture')
        model = ResourceGallery


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'is_available',
                  'address_line', 'type', 'country', 'state', 'city',
                  'picture')
        model = Resource


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'overview', 'status', 'start_date',
                  'end_date', 'resource', 'user')
        model = Reservation
