# Generated by Django 4.2.1 on 2023-09-18 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0032_alter_home_ctime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='cTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
