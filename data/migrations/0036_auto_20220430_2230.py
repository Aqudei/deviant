# Generated by Django 3.2.13 on 2022-04-30 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0035_alter_mytask_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='thank',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created At'),
        ),
        migrations.AddField(
            model_name='thank',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Updated At'),
        ),
    ]