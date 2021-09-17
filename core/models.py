from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class AvailableManager(models.Manager):
    """ A manager that return available resources """
    def get_queryset(self):
        return super(AvailableManager,
                     self).get_queryset().filter(is_available=True)


class ResourceType(models.Model):
    """ A type of resource model """
    _upload_link = 'images/resource_type'
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    picture = models.ImageField(null=True, blank=True, upload_to=_upload_link)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = _('Resource Type')
        verbose_name_plural = _('Resource Types')


class Resource(models.Model):
    """ A resource can be a house, car or anything that can be reserved """

    _upload_link = 'images/resource'

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
    picture = models.ImageField(blank=True, upload_to=_upload_link)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # I want to preserve the resource when the type they belong to is
    # deleted. Then use models.SET_NULL to allow resource without type
    type = models.ForeignKey(ResourceType,
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True)

    # Specify diferents managers that can be used by this model
    objects = models.Manager()  # The default manager.
    available = AvailableManager()  # Our custom manager.

    def get_absolute_url(self):
        type_slug = self.type.slug
        # We will use this method to link specific resource in template
        return reverse_lazy('core:resource_detail',
                            kwargs={
                                'type_slug': type_slug,
                                'resource_slug': self.slug
                            })

    def __str__(self) -> str:
        return _("{} ( {}€ / hour )").format(self.name, self.price)


class ResourceGallery(models.Model):
    """
        Each resource can have several gallry pictures.
    """

    _upload_link = 'images/resource_gallery'

    resource = models.ForeignKey(Resource,
                                 default=None,
                                 on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=_upload_link, max_length=200)

    def __str__(self) -> str:
        return _("Gallery picture {} for {}").format(self.id,
                                                     self.resource.name)

    class Meta:
        verbose_name = 'Resource Gallery'
        verbose_name_plural = 'Resource Galleries'


class Reservation(models.Model):
    """ A reservation model that used to reserve resources """

    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('in_progress', _('In Progress')),
        ('ended', _('Ended')),
        ('canceled', _('Canceled')),
    )
    title = models.CharField(max_length=200)
    overview = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=15,
                              choices=STATUS_CHOICES,
                              default='pending')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    resource = models.ForeignKey(Resource,
                                 default=None,
                                 on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='reservations',
                             default=1)

    def __str__(self) -> str:
        return _("{} - status : {}").format(self.title, self.status)