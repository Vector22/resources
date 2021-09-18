from django.contrib import admin
import admin_thumbnails

from core.models import Reservation, Resource, ResourceType, ResourceGallery

# Use memcache admin index site
admin.site.index_template = 'memcache_status/admin_index.html'


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'start_date', 'end_date')
    list_filter = ('status', )
    search_fields = (
        'title',
        'overview',
        'user',
    )
    date_hierarchy = 'created'
    ordering = ('status', 'created')
    readonly_fields = ('created', )


class ReservationInline(admin.TabularInline):
    model = Reservation
    fields = ('title', 'overview', 'status', 'user', 'start_date', 'end_date')
    extra = 1


# Resource Gallery
@admin.register(ResourceGallery)
@admin_thumbnails.thumbnail('picture')
class ResourceGalleryAdmin(admin.ModelAdmin):
    list_display = ('resource', 'picture_thumbnail')
    list_filter = ('resource', )


@admin_thumbnails.thumbnail('picture')
class ResourceGalleryInline(admin.TabularInline):
    model = ResourceGallery
    extra = 1  # Add only one extra field to add new image


@admin.register(Resource)
@admin_thumbnails.thumbnail('picture')
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available', 'address_line', 'city',
                    'picture_thumbnail')
    list_filter = ('type', )
    search_fields = (
        'name',
        'description',
    )
    date_hierarchy = 'created'
    ordering = ('created', 'name')
    readonly_fields = ('created', )
    prepopulated_fields = {'slug': ('name', )}
    inlines = [ResourceGalleryInline, ReservationInline]


@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'picture')
    search_fields = ('name', )
    date_hierarchy = 'created'
    ordering = ('created', 'name')
    readonly_fields = ('created', )
    prepopulated_fields = {'slug': ('name', )}
