# Generated by Django 3.1.6 on 2021-03-16 18:45

import cotizaciones.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('presupuestos', '0001_initial'),
        ('profesionales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('vencimiento', models.DateField(default=cotizaciones.models.get_vencimiento_defautl)),
                ('tipo', models.CharField(choices=[('M', 'Materiales'), ('S', 'Mano de obra')], default='M', max_length=1)),
                ('comentarios', models.TextField(blank=True, max_length=1000, null=True)),
                ('presupuesto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='presupuestos.presupuesto')),
                ('profesionales', models.ManyToManyField(blank=True, help_text='Los profesionales seleccionados serán notificados de la solicitud de cotización', to='profesionales.Profesional')),
                ('proveedores', models.ManyToManyField(blank=True, help_text='Los proveedores seleccionados serán notificados de la solicitud de cotización', to='profesionales.Proveedor')),
            ],
            options={
                'verbose_name': 'Solicitud de Cotización',
                'verbose_name_plural': 'Solicitudes de cotización',
                'unique_together': {('presupuesto', 'tipo')},
            },
        ),
        migrations.CreateModel(
            name='DetalleDeSolicitud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detalle_de_presupuesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='presupuestos.detalledepresupuesto')),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cotizaciones.solicitud')),
            ],
        ),
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('archivo', models.FileField(blank=True, null=True, upload_to='cotizaciones')),
                ('comentarios', models.TextField(blank=True, max_length=1000, null=True)),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cotizaciones.solicitud')),
            ],
            options={
                'verbose_name': 'Cotización',
                'verbose_name_plural': 'Cotizaciones',
            },
        ),
    ]
