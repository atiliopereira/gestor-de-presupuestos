# Generated by Django 3.1.6 on 2021-07-05 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotizaciones', '0005_auto_20210704_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='archivo',
            field=models.FileField(blank=True, help_text='Graficos, tablas o especificaciones adicionales.', null=True, upload_to='cotizaciones'),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='tipo',
            field=models.CharField(choices=[('M', 'Materiales'), ('S', 'Mano de obra')], default='M', max_length=1),
        ),
    ]
