"""Hotspots admin."""

# Django
from django.contrib import admin

# Model
from wapl.hotspots.models import Hotspot


@admin.register(Hotspot)
class HotspotAdmin(admin.ModelAdmin):
    """Hotspot admin."""

    list_display = (
        'name',
        'program',
        'installed_date',
        'lat',
        'long',
        'address',
        'mayoralty',
        'modified'
    )

    search_fields = ('name',)
    list_filter = ('program', 'mayoralty')
