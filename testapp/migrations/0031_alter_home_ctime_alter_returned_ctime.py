# Generated by Django 4.2.1 on 2023-09-18 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0030_home_ctime_returned_ctime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='cTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='returned',
            name='cTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
