from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from wapl.hotspots.api.views import HotspotViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("hotspot", HotspotViewSet)


app_name = "api"
urlpatterns = router.urls
