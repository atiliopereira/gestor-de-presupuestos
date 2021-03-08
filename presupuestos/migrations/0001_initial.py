# Generated by Django 3.1.6 on 2021-03-03 04:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('items', '0001_initial'),
        ('sistema', '0001_initial'),
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Presupuesto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('numero_de_presupuesto', models.CharField(max_length=100, verbose_name='Número de presupuesto')),
                ('obra', models.CharField(max_length=250, verbose_name='Nombre o Descripción')),
                ('direccion', models.CharField(blank=True, max_length=300, null=True, verbose_name='Dirección')),
                ('estado', models.CharField(choices=[('pen', 'Pendiente'), ('pre', 'Presupuestado'), ('env', 'Enviado al cliente'), ('rec', 'Rechazado'), ('apr', 'Aprobado')], default='pen', editable=False, max_length=3)),
                ('total', models.DecimalField(decimal_places=0, default=0, max_digits=15)),
                ('ciudad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sistema.ciudad')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clientes.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleDePresupuesto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.FloatField(default=1)),
                ('subtotal', models.DecimalField(decimal_places=0, default=0, max_digits=15)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='items.item')),
                ('presupuesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='presupuestos.presupuesto')),
            ],
        ),
    ]