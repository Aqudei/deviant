# Generated by Django 3.2.13 on 2022-04-16 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0031_mytask_last_ran'),
    ]

    operations = [
        migrations.AddField(
            model_name='mytask',
            name='last_error',
            field=models.TextField(blank=True, null=True, verbose_name='Last Error'),
        ),
    ]
