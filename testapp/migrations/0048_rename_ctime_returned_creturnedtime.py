# Generated by Django 4.2.7 on 2023-11-19 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0047_alter_returned_cnumber'),
    ]

    operations = [
        migrations.RenameField(
            model_name='returned',
            old_name='cTime',
            new_name='cReturnedTime',
        ),
    ]
