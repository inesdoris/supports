from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profil', views.profil, name='profil'),
    path('utilisateur/ajout', views.ajout_utilisateur, name='ajout_utilisateur'),
    path('utilisateur/liste', views.liste_utilisateur, name='liste_utilisateur'),
    path('utilisateur/<int:id>/modifier', views.modifier_utilisateur, name='modifier_utilisateur'),
    path('utilisateur/<int:id>/supprimer', views.supprimer_utilisateur, name='supprimer_utilisateur'),

    path('agence/ajout', views.ajout_agence, name='ajout_agence'),
    path('agence/liste', views.liste_agence, name='liste_agence'),
    path('agence/<int:id>/modifier', views.modifier_agence, name='modifier_agence'),
    path('agence/<int:id>/supprimer', views.supprimer_agence, name='supprimer_agence'),
    
    path('chef_agence/formulaire', views.formulaire, name='formulaire'),
]
