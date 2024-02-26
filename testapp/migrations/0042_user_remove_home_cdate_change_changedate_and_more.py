# Generated by Django 4.2.1 on 2023-11-04 09:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0041_alter_home_ccount'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20)),
                ('username', models.CharField(default='', max_length=20)),
                ('password', models.CharField(default='', max_length=20)),
                ('title', models.CharField(default='', max_length=20)),
                ('ispro', models.CharField(default='', max_length=20)),
                ('Position', models.CharField(default='', max_length=20)),
                ('UserTime', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='home',
            name='cDate',
        ),
        migrations.AddField(
            model_name='change',
            name='ChangeDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='contact',
            name='ContactDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='contract',
            name='ContractDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='contractinner',
            name='ContractInnerDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='home',
            name='HomeDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='meeting',
            name='MeetingDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='meetinginner',
            name='MeetingInnerDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='returned',
            name='ReturnedDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='signed',
            name='SignedDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='home',
            name='cProgress',
            field=models.CharField(choices=[('草稿', '草稿'), ('流程中', '流程中'), ('結案', '結案')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='transfered',
            name='cTransferTo',
            field=models.CharField(max_length=20),
        ),
    ]