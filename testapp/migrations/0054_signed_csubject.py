# Generated by Django 4.2.1 on 2024-01-18 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0053_remove_signed_csubject_home_csubject'),
    ]

    operations = [
        migrations.AddField(
            model_name='signed',
            name='cSubject',
            field=models.CharField(default='', max_length=255),
        ),
    ]
