# Generated by Django 2.0 on 2018-05-17 13:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2018, 5, 17, 16, 59, 48, 23661), verbose_name='Опубликована'),
        ),
    ]
