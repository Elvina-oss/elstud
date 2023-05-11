import requests
from django.conf import settings
from django.db import models

from elstud.settings import OPENCAGE_API_KEY


class Event(models.Model):
    tittle = models.CharField(max_length=200, verbose_name='Название')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    latitude = models.FloatField(null=True, blank=True, verbose_name='Широта')
    longitude = models.FloatField(null=True, blank=True, verbose_name='Долгота')
    type = models.CharField(max_length=100, verbose_name='Тип мероприятия')
    image = models.ImageField(blank=True, upload_to='events', verbose_name='Фото')
    time = models.DateTimeField(verbose_name='Дата и время')
    description = models.TextField(verbose_name='Описание')


    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            # If latitude and longitude are not already set, geocode the address
            address = self.address
            url = f'https://api.opencagedata.com/geocode/v1/json?q={address}&key={OPENCAGE_API_KEY}'
            response = requests.get(url)
            if response.status_code == 200:
                result = response.json()
                if len(result['results']) > 0:
                    # Set the latitude and longitude based on the first result
                    geometry = result['results'][0]['geometry']
                    self.latitude = geometry['lat']
                    self.longitude = geometry['lng']
        super().save(*args, **kwargs)

class EventVisitor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    assurance = models.BooleanField(default=False)