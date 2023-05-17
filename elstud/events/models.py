import requests
from django.conf import settings
from django.db import models




class Event(models.Model):
    tittle = models.CharField(max_length=200, verbose_name='Название')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    latitude = models.FloatField(null=True, blank=True, verbose_name='Широта')
    longitude = models.FloatField(null=True, blank=True, verbose_name='Долгота')
    type = models.CharField(max_length=100, blank=True, verbose_name='Тип мероприятия')
    image = models.ImageField(blank=True, upload_to='images/events/', verbose_name='Фото')
    time = models.DateTimeField(verbose_name='Дата и время')
    description = models.TextField(verbose_name='Описание')




class EventVisitor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    assurance = models.BooleanField(default=False)