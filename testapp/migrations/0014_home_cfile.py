# Generated by Django 4.2.1 on 2023-06-09 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0013_alter_home_creceive'),
    ]

    operations = [
        migrations.AddField(
            model_name='home',
            name='cFile',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]