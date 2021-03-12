# Generated by Django 3.1.6 on 2021-03-12 02:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre o Razón social')),
                ('ruc', models.CharField(blank=True, max_length=20, null=True, verbose_name='RUC')),
                ('direccion', models.CharField(blank=True, max_length=200, null=True, verbose_name='dirección')),
                ('telefono', models.CharField(blank=True, max_length=50, null=True, verbose_name='teléfono')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, verbose_name='e-mail')),
                ('creado_por', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
