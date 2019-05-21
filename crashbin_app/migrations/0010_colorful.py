# Generated by Django 2.2.1 on 2019-05-21 14:29

import colorful.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crashbin_app', '0009_unique_names'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='color',
            field=colorful.fields.RGBColorField(colors=['#0033CC', '#428BCA', '#44AD8E', '#A8D695', '#5CB85C', '#69D100', '#004E00', '#34495E', '#7F8C8D', '#A295D6', '#5843AD', '#8E44AD', '#FFECDB', '#AD4363', '#D10069', '#CC0033', '#FF0000', '#D9534F', '#D1D100', '#F0AD4E', '#AD8D43']),
        ),
    ]