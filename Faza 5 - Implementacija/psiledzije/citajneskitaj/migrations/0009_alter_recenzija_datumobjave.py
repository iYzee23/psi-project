# Generated by Django 4.2.1 on 2023-06-02 19:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citajneskitaj', '0008_alter_recenzija_datumobjave'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recenzija',
            name='datumobjave',
            field=models.DateTimeField(db_column='DatumObjave', default=datetime.datetime(2023, 6, 2, 21, 7, 18, 590813)),
        ),
    ]