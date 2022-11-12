# Generated by Django 3.2.13 on 2022-11-12 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0036_auto_20220430_2230'),
    ]

    operations = [
        migrations.CreateModel(
            name='HookRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('body', models.TextField(verbose_name='Body')),
                ('headers', models.TextField(verbose_name='Headers')),
            ],
            options={
                'verbose_name': 'hookrequest',
                'verbose_name_plural': 'hookrequests',
            },
        ),
        migrations.CreateModel(
            name='Webhook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trigger', models.CharField(max_length=100, verbose_name='Trigger')),
                ('url', models.URLField(max_length=400, verbose_name='Url')),
            ],
            options={
                'verbose_name': 'webhooh',
                'verbose_name_plural': 'webhoohs',
            },
        ),
        migrations.AddField(
            model_name='deviation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created At'),
        ),
        migrations.AddField(
            model_name='deviation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Updated At'),
        ),
        migrations.AddField(
            model_name='user',
            name='patreon_token',
            field=models.JSONField(blank=True, null=True, verbose_name='Patreon Token'),
        ),
    ]
