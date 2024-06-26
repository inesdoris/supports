# Generated by Django 5.0.4 on 2024-04-26 08:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CategorieService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EtatDemande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Chef_Agence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('sexe', models.BooleanField(default=True)),
                ('adresse', models.CharField(max_length=30)),
                ('contact', models.CharField(max_length=20, unique=True)),
                ('agence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.agence')),
            ],
        ),
        migrations.CreateModel(
            name='Demande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=150)),
                ('date_formulation', models.DateTimeField(auto_now_add=True)),
                ('demandeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.chef_agence')),
                ('etat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.etatdemande')),
            ],
        ),
        migrations.CreateModel(
            name='MessageDemande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('date_envoi', models.DateTimeField(auto_now_add=True)),
                ('demande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.demande')),
            ],
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('sexe', models.BooleanField(default=True)),
                ('adresse', models.CharField(max_length=30)),
                ('contact', models.CharField(max_length=20, unique=True)),
                ('agence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.agence')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.section')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.categorieservice')),
            ],
        ),
        migrations.AddField(
            model_name='demande',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='support.service'),
        ),
        migrations.CreateModel(
            name='traiter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution', models.CharField(default=True, max_length=200)),
                ('date_traitement', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='support.agent')),
                ('demande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.demande')),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('profil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.profil')),
            ],
        ),
    ]
