# Generated by Django 4.2.2 on 2023-06-06 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citajneskitaj', '0010_alter_recenzija_datumobjave'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knjiga',
            name='opis',
            field=models.CharField(blank=True, db_column='Opis', max_length=1000, null=True),
        ),
    ]