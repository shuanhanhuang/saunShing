# Generated by Django 4.2.1 on 2023-09-19 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0038_home_ccount_alter_returned_ctime_transfered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfered',
            name='cTransferTo',
            field=models.CharField(choices=[('None', '無'), ('郭文龍', '郭文龍'), ('侯國興', '侯國興'), ('郭文河', '郭文河'), ('高晟琅', '高晟琅'), ('黃睿堂', '黃睿堂'), ('鄭任雯', '鄭任雯'), ('高麗華', '高麗華'), ('侯宗仁', '侯宗仁'), ('黃美禎', '黃美禎'), ('江水木', '江水木'), ('吳建進', '吳建進'), ('陳佳欣', '陳佳欣'), ('蔡孟亭', '蔡孟亭'), ('馮文明', '馮文明'), ('陳恆瑞', '陳恆瑞'), ('郭文欽', '郭文欽'), ('陳春能', '陳春能'), ('黃春北', '黃春北')], max_length=20),
        ),
    ]
