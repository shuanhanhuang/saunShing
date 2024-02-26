# Generated by Django 4.2.1 on 2023-11-04 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0042_user_remove_home_cdate_change_changedate_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='change',
            table='Change',
        ),
        migrations.AlterModelTable(
            name='contact',
            table='Contact',
        ),
        migrations.AlterModelTable(
            name='contract',
            table='Contract',
        ),
        migrations.AlterModelTable(
            name='contractinner',
            table='ContractInner',
        ),
        migrations.AlterModelTable(
            name='count',
            table='Count',
        ),
        migrations.AlterModelTable(
            name='home',
            table='Home',
        ),
        migrations.AlterModelTable(
            name='meeting',
            table='Meeting',
        ),
        migrations.AlterModelTable(
            name='meetinginner',
            table='MeetingInner',
        ),
        migrations.AlterModelTable(
            name='returned',
            table='Returned',
        ),
        migrations.AlterModelTable(
            name='signed',
            table='Signed',
        ),
        migrations.AlterModelTable(
            name='transfered',
            table='Transfer',
        ),
        migrations.AlterModelTable(
            name='user',
            table='User',
        ),
    ]
