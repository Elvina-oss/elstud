import requests
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from account.models import UserProfile


class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL', blank=True)
    address = models.CharField(max_length=200, verbose_name='Адрес')
    latitude = models.FloatField(null=True, blank=True, verbose_name='Широта')
    longitude = models.FloatField(null=True, blank=True, verbose_name='Долгота')
    type = models.CharField(max_length=100, blank=True, verbose_name='Тип мероприятия')
    image = models.ImageField(blank=True, upload_to='images/events/', verbose_name='Фото')
    time_start = models.DateTimeField(verbose_name='Дата и время начала')
    time_end = models.DateTimeField(verbose_name='Дата и время окончания')
    approved = models.BooleanField(default=False)
    description = models.TextField(verbose_name='Описание')
    organizator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title + str(self.pk))
        super(Event, self).save(*args, **kwargs)


class EventVisitor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    assurance = models.BooleanField(default=False)