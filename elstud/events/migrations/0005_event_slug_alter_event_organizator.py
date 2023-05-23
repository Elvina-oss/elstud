# Generated by Django 4.1.7 on 2023-05-21 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_userprofile_image'),
        ('events', '0004_event_organizator'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='event',
            name='organizator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.userprofile'),
        ),
    ]
