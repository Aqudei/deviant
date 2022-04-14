# Generated by Django 3.2.13 on 2022-04-14 06:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0021_thank_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('da_username', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Deviant Username')),
                ('da_userid', models.CharField(blank=True, max_length=100, null=True, verbose_name='DA User Id')),
                ('perc_shared_watchers', models.FloatField(default=0.0, verbose_name='Percent Shared Watchers')),
                ('total_submission', models.IntegerField(default=0, verbose_name='Total Submissions')),
                ('total_watchers', models.IntegerField(default=0, verbose_name='Total Watchers')),
                ('total_pageviews', models.IntegerField(default=0, verbose_name='Total Pageviews')),
                ('date_started', models.DateTimeField(blank=True, null=True, verbose_name='Date Started')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'competitor',
                'verbose_name_plural': 'competitors',
            },
        ),
    ]
