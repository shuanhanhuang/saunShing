# Generated by Django 4.2.1 on 2023-09-18 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0033_alter_home_ctime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='cTime',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='returned',
            name='cTime',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]