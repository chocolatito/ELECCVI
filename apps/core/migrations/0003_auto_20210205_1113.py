# Generated by Django 3.0 on 2021-02-05 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_voto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voto',
            name='candidato',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Candidato'),
        ),
    ]