# Generated by Django 3.1.6 on 2021-05-04 19:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cotizaciones', '0002_materialdecotizacion_serviciodecotizacion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='materialdecotizacion',
            options={'verbose_name_plural': 'Materiales de la Cotizaciones'},
        ),
        migrations.AlterModelOptions(
            name='serviciodecotizacion',
            options={'verbose_name_plural': 'Servicios de la Cotizaciones'},
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='creado_por',
            field=models.ForeignKey(default=1, editable=False, on_delete=django.db.models.deletion.PROTECT, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='materialdecotizacion',
            name='precio',
            field=models.DecimalField(decimal_places=0, default=0, help_text='Indicar el precio unitario', max_digits=15, verbose_name='Precio Unitario'),
        ),
        migrations.AlterField(
            model_name='serviciodecotizacion',
            name='precio',
            field=models.DecimalField(decimal_places=0, default=0, help_text='Indicar el precio unitario', max_digits=15, verbose_name='Precio Unitario'),
        ),
    ]
