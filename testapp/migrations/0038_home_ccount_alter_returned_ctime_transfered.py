# Generated by Django 4.2.1 on 2023-09-19 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0037_home_ctime'),
    ]

    operations = [
        migrations.AddField(
            model_name='home',
            name='cCount',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='returned',
            name='cTime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Transfered',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cTransferTo', models.CharField(blank=True, choices=[('None', '無'), ('郭文龍', '郭文龍'), ('侯國興', '侯國興'), ('郭文河', '郭文河'), ('高晟琅', '高晟琅'), ('黃睿堂', '黃睿堂'), ('鄭任雯', '鄭任雯'), ('高麗華', '高麗華'), ('侯宗仁', '侯宗仁'), ('黃美禎', '黃美禎'), ('江水木', '江水木'), ('吳建進', '吳建進'), ('陳佳欣', '陳佳欣'), ('蔡孟亭', '蔡孟亭'), ('馮文明', '馮文明'), ('陳恆瑞', '陳恆瑞'), ('郭文欽', '郭文欽'), ('陳春能', '陳春能'), ('黃春北', '黃春北')], max_length=20, null=True)),
                ('transferhome', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='detailes', to='testapp.home')),
            ],
        ),
    ]