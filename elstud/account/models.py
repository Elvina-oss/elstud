
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# passwords for Иван 5vi-pCa-Pjr-YAd
# AAAbramov152.12 f6t-YYs-bLL-S5u

# BBBorisov  Y2QmI1ah

# PNatalie qO0fNTh7
from django.urls import reverse
from django.utils.text import slugify


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    is_student = models.BooleanField(default=True, verbose_name='Студент')
    group = models.CharField(max_length=20, blank=True, verbose_name='Номер группы')
    organization_name = models.CharField(max_length=50, blank=True, verbose_name='Название организации')
    image = models.ImageField(upload_to='images/profiles', blank=True, verbose_name='Фото')

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        user = self.user
        return user.first_name + ' ' + user.last_name

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

