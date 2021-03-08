# Generated by Django 3.1.6 on 2021-03-07 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presupuestos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='estado',
            field=models.CharField(choices=[('pen', 'Pendiente'), ('env', 'Enviado al cliente'), ('rec', 'Rechazado'), ('apr', 'Aprobado')], default='pen', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='numero_de_presupuesto',
            field=models.CharField(editable=False, max_length=100, verbose_name='Número de presupuesto'),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='obra',
            field=models.CharField(help_text='Nombre o Descripción', max_length=250),
        ),
    ]