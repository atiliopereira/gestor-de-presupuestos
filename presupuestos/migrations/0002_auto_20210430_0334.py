# Generated by Django 3.1.6 on 2021-04-30 07:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presupuestos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='margen_de_ganancia',
            field=models.PositiveSmallIntegerField(default=0, help_text='0 a 100', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='observaciones',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='validez_del_presupuesto',
            field=models.PositiveSmallIntegerField(default=30, help_text='Vigencia en días'),
        ),
    ]