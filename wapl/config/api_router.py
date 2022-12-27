from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from wapl.hotspots.api.views import HotspotsViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("hotspots", HotspotsViewSet)


app_name = "api"
urlpatterns = router.urls
