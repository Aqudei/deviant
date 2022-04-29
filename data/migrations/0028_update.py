# Generated by Django 3.2.13 on 2022-04-16 03:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0027_alter_competitor_watchers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('COMPETITORS', 'COMPETITORS'), ('FAVOURITES', 'FAVOURITES'), ('WATCHERS', 'WATCHERS')], max_length=50, verbose_name='Name')),
                ('last_update', models.DateTimeField(auto_now_add=True, verbose_name='Last Update')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'update',
                'verbose_name_plural': 'updates',
            },
        ),
    ]