"""Hotspot Celery tasks."""

# Django

# Celery
from config import celery_app
from celery.schedules import crontab

# Hotspot
from wapl.hotspots.models import Hotspot

# Utilities
from config.settings.base import ORIGIN_DATA_URL
import requests
import tempfile
import lxml.html as html
import csv


@celery_app.on_after_finalize.connect
def setup_hotspot_periodic_task(sender, **kwargs):
    # pass
    sender.add_periodic_task(
        crontab(minute="*/10"),
        get_hotspots.s(),
    )


@celery_app.task(soft_time_limit=7*60)
def get_hotspots():
    XPATH_DOWNLOAD_CSV_URL = '//section[@id="dataset-resources"]//div/a[last()]/@href'

    response = requests.get(ORIGIN_DATA_URL)
    if response.status_code == 200:
        page = response.content.decode('utf-8')
        parsed = html.fromstring(page)
        download_url = parsed.xpath(XPATH_DOWNLOAD_CSV_URL)[0]
        file = tempfile.TemporaryFile(mode="w+t")

        download = requests.get(download_url)
        file.write(download.content.decode('utf-8'))

        file.seek(0)

        csv_data = csv.DictReader(file, delimiter=',')

        for hotspot in csv_data:
            Hotspot.objects.update_or_create(
                name=hotspot["id"],
                defaults={
                    "program": hotspot["programa"],
                    "installed_date": hotspot["fecha_instalacion"],
                    "lat": hotspot["latitud"],
                    "long": hotspot["longitud"],
                    "address": hotspot["colonia"],
                    "mayoralty": hotspot["alcaldia"]
                }
            )
        file.close()
    else:
        raise ValueError(f'Error: {response.status_code}')
