# Generated by Django 3.0.8 on 2020-08-06 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_auth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='email',
        ),
    ]
