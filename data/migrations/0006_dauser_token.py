# Generated by Django 4.0.2 on 2022-03-06 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_alter_dauser_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='dauser',
            name='token',
            field=models.JSONField(blank=True, null=True, verbose_name='Token'),
        ),
    ]