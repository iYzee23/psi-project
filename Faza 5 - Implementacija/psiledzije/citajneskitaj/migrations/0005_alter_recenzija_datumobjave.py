# Generated by Django 4.2.1 on 2023-05-30 11:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citajneskitaj', '0004_alter_recenzija_datumobjave'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recenzija',
            name='datumobjave',
            field=models.DateTimeField(db_column='DatumObjave', default=datetime.datetime(2023, 5, 30, 13, 9, 32, 761907)),
        ),
    ]