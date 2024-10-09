# Generated by Django 5.1.1 on 2024-10-06 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fin_app_v2', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='client',
        ),
        migrations.AddField(
            model_name='job',
            name='client_email',
            field=models.EmailField(default=11, max_length=254, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='client_password',
            field=models.CharField(default=12212112, max_length=100),
            preserve_default=False,
        ),
    ]