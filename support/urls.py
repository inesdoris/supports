from django.contrib import admin
from django.urls import path, include
from . import views
from . import agent_views

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
    path('chef_agence/dashboard', views.chef_agence_dashboard, name='dashboard'),
    path('chef_agence/demandes_en_attente', views.chef_agence_demandes_en_attente, name='demandes_en_attente'),
    path('chef_agence/demandes_resolues', views.chef_agence_demandes_resolues, name='demandes_resolues'),
    path('demande/<int:id>/consulter', views.consulter_demande, name='consulter_demande'),
    path('chef_agence/<int:demande_id>/modifier_demande', views.modifier_demande, name='modifier_demande'),
    path('chef_agence/<int:id>/supprimer_demande', views.supprimer_demande, name='supprimer_demande'),

    path('notifications', views.notifications, name='notifications'),
    path('notifications/<int:id>/supprimer', views.supprimer_notification, name='supprimer_notification'),

    # views for agent
    path('agent/', agent_views.index, name='agent-homepage'),
    path('agent/pending', agent_views.pending, name='demandes-en-cours-de-traitement'),
    path('agent/solved', agent_views.solved, name='demandes-resolues'),
    path('agent/<int:id_demande>', agent_views.mettre_en_traitement, name='mettre-une-demande-en-cours-de-traitement'),
<<<<<<< HEAD
<<<<<<< HEAD
    path('agent/<int:id_demande>/categorize', agent_views.categoriser_demande, name='categoriser-une-demande'),
    path('agent/pending/<int:id_demande>', agent_views.traiter_demande, name='traiter-une-demande'),
    path('agent/solved/<int:id_demande>', agent_views.consulter_demande, name='consulter-une-demande'),
=======
    path('agent/<int:id_demande>/treat', agent_views.abolir_traitement, name='mettre-une-demande-en-fin-de-traitement'),
    path('agent/<int:id_demande>/categorize', agent_views.categoriser_demande, name='categoriser-une-demande'),
    path('agent/<int:id_demande>/categorize', agent_views.categoriser_demande, name='categoriser-une-demande'),
    path('agent/pending/<int:id_demande>', agent_views.traiter_demande, name='traiter-une-demande'),
    path('agent/solved/<int:id_demande>', agent_views.consulter_demande, name='consulter-une-demande'),
    path('agent/admin/', agent_views.admin, name='messages-envoyees-a-l-admin'),
    path('agent/admin/<int:id_demande>', agent_views.notifier_admin, name='envoi-admin'),
>>>>>>> dev_ange
=======
    path('agent/<int:id_demande>/categorize', agent_views.categoriser_demande, name='categoriser-une-demande'),
    path('agent/pending/<int:id_demande>', agent_views.traiter_demande, name='traiter-une-demande'),
    path('agent/solved/<int:id_demande>', agent_views.consulter_demande, name='consulter-une-demande'),
>>>>>>> bfa885662b246bf6825714b3ab754268d09bc098
    
    # views for admin
    path('demande/recues', views.liste_demandes_recues, name='liste_demandes_recues'),
    path('demande/affectees', views.liste_demandes_affectees, name='liste_demandes_affectees'),
    path('demande/traitees', views.liste_demandes_traitees, name='liste_demandes_traitees'),
    path('demande/<int:demande_id>/affecter_agent', views.affecter_agent, name='affecter_agent'),
    path('demande/<int:demande_id>/envoyer_solution', views.envoyer_solution, name='envoyer_solution'),
]
