# Generated by Django 3.1.6 on 2021-02-17 20:59
# Generated by Django 3.1.6 on 2021-02-17 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('materiales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rubro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200, verbose_name='descripción')),
                ('rubro', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='items.rubro')),
                ('unidad_de_medida', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='materiales.unidaddemedida')),
            ],
            options={
                'verbose_name': 'ítem',
                'verbose_name_plural': 'ítems',
            },
        ),
        migrations.CreateModel(
            name='DetalleDeItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coeficiente', models.FloatField(default=1.0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.item')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='materiales.material')),
            ],
            options={
                'verbose_name': 'detalle de ítem',
                'verbose_name_plural': 'detalles de ítem',
            },
        ),
    ]
