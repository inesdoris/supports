# Generated by Django 5.0.4 on 2024-05-22 11:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0004_demande_agent_alter_utilisateur_agence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='categorie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='support.categorieservice'),
        ),
    ]