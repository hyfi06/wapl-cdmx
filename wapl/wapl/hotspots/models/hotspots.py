"""Hotspots model."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from wapl.utils.models import BaseModel
import math


class Hotspot(BaseModel):
    """Hotsport model.
    A hotsport wifi is a wifi access point locate in a site.  
    """

    name = models.CharField(
        verbose_name=_("Hotspot ID"),
        max_length=130,
        unique=True
    )

    program = models.CharField(
        verbose_name=_("Program"),
        max_length=60,
    )

    installed_date = models.DateField(
        verbose_name=_("Installed date")
    )

    lat = models.FloatField(
        verbose_name=_("Latitude"),
        blank=False
    )

    long = models.FloatField(
        verbose_name=_("Longitude"),
        blank=False
    )

    address = models.CharField(
        verbose_name=_("Address"),
        max_length=100,
    )

    mayoralty = models.CharField(
        verbose_name=_("Mayoralty"),
        max_length=100,
    )

    def __str__(self) -> str:
        return self.name

    def distance(self, lat: float, long: float) -> float:
        return math.sqrt(
            (lat - self.lat) ** 2 +
            (long - self.long)**2
        )
