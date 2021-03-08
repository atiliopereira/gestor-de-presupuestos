# Generated by Django 3.1.6 on 2021-02-19 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0002_auto_20210218_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actualizaciondeprecios',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='planillas_de_precios'),
        ),
        migrations.AlterField(
            model_name='preciodematerial',
            name='fin_de_vigencia',
            field=models.DateField(blank=True, editable=False, null=True),
        ),
    ]
