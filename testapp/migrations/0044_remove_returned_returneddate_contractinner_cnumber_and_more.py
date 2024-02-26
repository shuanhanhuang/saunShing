# Generated by Django 4.2.1 on 2023-11-16 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0043_alter_change_table_alter_contact_table_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='returned',
            name='ReturnedDate',
        ),
        migrations.AddField(
            model_name='contractinner',
            name='cNumber',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='home',
            name='HomeTime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='meetinginner',
            name='cNumber',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='returned',
            name='cNumber',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='change',
            name='ChangeDate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='ContactDate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='ContractDate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='contractinner',
            name='ContractInnerDate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='MeetingDate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='meetinginner',
            name='MeetingInnerDate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='signed',
            name='SignedDate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='UserTime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
