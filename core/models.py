from django.db import models
from django.urls import reverse_lazy


class AvailableManager(models.Manager):
    """ A manager that return available resources """
    def get_queryset(self):
        return super(AvailableManager,
                     self).get_queryset().filter(is_available=True)


class ResourceType(models.Model):
    """ A type of resource model """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)


class Resource(models.Model):
    """ A resource can be a house, car or anything that can be reserved """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    # This price is per hour of usage
    price = models.IntegerField()
    is_available = models.BooleanField(default=True)
    address_line = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    picture = models.ImageField(blank=True, upload_to='images/resources')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # I want to preserve the resource when the type they belong to is
    # deleted. Then use models.SET_NULL to allow resource without type
    type = models.ForeignKey(ResourceType,
                             models.SET_NULL,
                             blank=True,
                             null=True)

    # Specify diferents managers that can be used by this model
    objects = models.Manager()  # The default manager.
    available = AvailableManager()  # Our custom manager.

    def get_absolute_url(self):
        # We will use this method to link specific resource in template
        return reverse_lazy('core:resource_detail',
                            kwargs={
                                'type_slug': self.type.slug,
                                'resource_slug': self.slug
                            })

    def __str__(self):
        return f"{self.name} - {self.price}€ / per hour."
