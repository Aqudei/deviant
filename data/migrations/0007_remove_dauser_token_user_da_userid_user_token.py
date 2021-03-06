# Generated by Django 4.0.2 on 2022-03-06 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_dauser_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dauser',
            name='token',
        ),
        migrations.AddField(
            model_name='user',
            name='da_userid',
            field=models.UUIDField(blank=True, null=True, verbose_name='DA User Id'),
        ),
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.JSONField(blank=True, null=True, verbose_name='Token'),
        ),
    ]
