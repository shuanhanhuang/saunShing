# Generated by Django 4.2.1 on 2023-09-19 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0039_alter_transfered_ctransferto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='cReceive',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]