# Generated by Django 4.2.1 on 2023-09-18 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0035_alter_home_ctime_alter_returned_ctime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='home',
            name='cTime',
        ),
    ]
