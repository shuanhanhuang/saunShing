# Generated by Django 4.2.1 on 2024-04-07 03:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0072_agent'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Agent',
            new_name='pchange',
        ),
        migrations.AlterModelTable(
            name='pchange',
            table='pchange',
        ),
    ]