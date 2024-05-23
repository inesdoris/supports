from django.db import models
from .utils import *
from django.utils import timezone


# Create your models here.
class Profil(models.Model):
    libelle = models.CharField(max_length=100)


class Agence(models.Model):
    nom = models.CharField(max_length=100)


class Section(models.Model):
    nom = models.CharField(max_length=100)


class Utilisateur(models.Model):
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    nom = models.CharField(max_length=100, default=True)
    prenom = models.CharField(max_length=100, default=True)
    email = models.EmailField(max_length=20, default=True)
    sexe = models.BooleanField(default=True)  # par défaut, c'est un homme
    adresse = models.CharField(max_length=30, default=True)
    contact = models.CharField(max_length=20, unique=True, default=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE)
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)

    def true_pass(self):
        return dechiffrement(self.password)
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"


class EtatDemande(models.Model):
    libelle = models.CharField(max_length=100)


class CategorieService(models.Model):
    libelle = models.CharField(max_length=100)


class Service(models.Model):
    libelle = models.CharField(max_length=100)
    categorie = models.ForeignKey(CategorieService, on_delete=models.CASCADE, null=True, blank=False)
    
    def __str__(self):
        return f"{self.libelle}"


class Demande(models.Model): 
    description = models.CharField(max_length=150)
    etat = models.ForeignKey(EtatDemande, on_delete=models.CASCADE)
    demandeur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    date_formulation = models.DateTimeField(default=timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()))
    agent = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, related_name='assigned_demandes', null=True, blank=True)

class MessageDemande(models.Model):
    contenu = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE)
    date_envoi = models.DateTimeField(default=timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()))


class Traiter(models.Model):
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, default=True)
    solution = models.CharField(max_length=200, default=True)
    date_traitement = models.DateTimeField(default=timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()))


class Notifications(models.Model):
    message = models.CharField(max_length=200)
    receiver = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_notification = models.DateTimeField(default=timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()))
    is_read = models.BooleanField(default=False)
