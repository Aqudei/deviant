# Generated by Django 4.0.3 on 2022-03-10 03:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0011_deviation_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='favor',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
    ]