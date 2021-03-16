# Generated by Django 3.1.6 on 2021-03-12 02:59

import datetime
from django.db import migrations, models
import django.db.models.deletion
import servicios.models
import sistema.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('materiales', '0001_initial'),
        ('sistema', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActualizacionDePreciosDeServicios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('archivo', models.FileField(blank=True, null=True, upload_to='planillas_de_precios')),
            ],
            options={
                'verbose_name': 'actualización de precios',
                'verbose_name_plural': 'actualizaciones de precios',
            },
        ),
        migrations.CreateModel(
            name='CategoriaDeServicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('categoria_padre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='categoria', to='servicios.categoriadeservicio', verbose_name='Categoría')),
                ('categoria_principal', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='categoria_raiz', to='servicios.categoriadeservicio', verbose_name='Categoría Principal')),
            ],
            options={
                'verbose_name': 'categoría de servicios',
                'verbose_name_plural': 'categorías de servicios',
            },
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=50, verbose_name='código')),
                ('descripcion', models.CharField(max_length=150, verbose_name='descripción')),
                ('categoria', models.ForeignKey(default=servicios.models.get_default_cat_de_servicio, on_delete=django.db.models.deletion.PROTECT, to='servicios.categoriadeservicio', verbose_name='categoría')),
                ('unidad_de_medida', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='materiales.unidaddemedida')),
            ],
        ),
        migrations.CreateModel(
            name='PrecioDeServicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=0, max_digits=15)),
                ('inicio_de_vigencia', models.DateField(default=datetime.date.today)),
                ('fin_de_vigencia', models.DateField(blank=True, editable=False, null=True)),
                ('ciudad', models.ForeignKey(default=sistema.models.get_ciudad_default, on_delete=django.db.models.deletion.PROTECT, to='sistema.ciudad')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicios.servicio')),
            ],
            options={
                'verbose_name_plural': 'Precios de servicios',
            },
        ),
    ]