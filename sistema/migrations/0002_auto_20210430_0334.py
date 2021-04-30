# Generated by Django 3.1.6 on 2021-04-30 07:34

from django.db import migrations, models
import django.db.models.deletion
import sistema.models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='ciudad',
            field=models.ForeignKey(default=sistema.models.get_ciudad_default, on_delete=django.db.models.deletion.PROTECT, to='sistema.ciudad'),
        ),
    ]
