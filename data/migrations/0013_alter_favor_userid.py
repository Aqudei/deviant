# Generated by Django 4.0.3 on 2022-03-10 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0012_favor_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favor',
            name='userid',
            field=models.UUIDField(blank=True, null=True, verbose_name='User Id'),
        ),
    ]
