# Generated by Django 4.2.1 on 2023-09-07 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0028_remove_signed_ccheck'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='change',
            name='cApproved',
        ),
        migrations.RemoveField(
            model_name='change',
            name='cReview',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='cOption',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='cDepartmentManager_Sign',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='cGeneral_Sign',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='cManager_Sign',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='cViceGeneral_Sign',
        ),
        migrations.RemoveField(
            model_name='home',
            name='cLock',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='cManger_Sign',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='cViceGeneral_Sign',
        ),
    ]