# Generated by Django 4.0.2 on 2022-02-12 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_alter_dauser_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dauser',
            options={'verbose_name': 'Watcher', 'verbose_name_plural': 'Watchers'},
        ),
    ]
