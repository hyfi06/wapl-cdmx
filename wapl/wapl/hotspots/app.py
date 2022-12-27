"""hotspots app"""

# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HotspotsConfig(AppConfig):
    name = "wapl.hotspots"
    verbose_name = _("Hotspots")

    def ready(self):
        try:
            import wapl.hotspots.signals  # noqa F401
        except ImportError:
            pass
