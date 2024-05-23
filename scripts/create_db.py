from support.models import *

def run():
    ############# PROFIL
    p = Profil(libelle="ADMINISTRATEUR")
    p.save()

    p = Profil(libelle="AGENT")
    p.save()

    p = Profil(libelle="CHEF AGENCE")
    p.save()

    ############# AGENCE
    a = Agence(nom="AC - AVRANKOU")
    a.save()

    a = Agence(nom="AC - PAHOU")
    a.save()

    a = Agence(nom="AC - AMOMEY CALAVI")
    a.save()

    ############ SECTION
    s = Section(nom="Application")
    s.save()

    s = Section(nom="Réseau et maintenance")
    s.save()

    ########### UTILISATEUR
    u = Utilisateur(login="aa", password="tt", nom="DOE", prenom="John", email="test@gmail.com", sexe=True, adresse="Akpakpa", contact="+2290095959855", profil_id=1, agence_id=1)
    u.save()

    u = Utilisateur(login="paul", password="itne", nom="DOSSOU", prenom="Firmine", email="firmine@gmail.com", sexe=False, adresse="Ouidah", contact="+22987412563", profil_id=3, agence_id=2)
    u.save()

    u = Utilisateur(login="lucio", password="envbh", nom="TOPANOU", prenom="Ludel", email="ludel@gmail.com", sexe=True, adresse="Calavi", contact="+22961012344", profil_id=2, agence_id=3, section_id=1)
    u.save()

    ########### CATEGORIE
    c = CategorieService(libelle="Application web")
    c.save()

    c = CategorieService(libelle="Réseaux")
    c.save()

    c = CategorieService(libelle="Systèmes")
    c.save()

    c = CategorieService(libelle="Maintenance")
    c.save()

    ########### SERVICE
    sv = Service(libelle="Création d'une application web", categorie_id=1)
    sv.save()

    sv = Service(libelle="Réparation de câbles réseaux", categorie_id=2)
    sv.save()

    sv = Service(libelle="Rétablissement de la connexion", categorie_id=2)
    sv.save()

    sv = Service(libelle="Installation de systèmes d'exploitation", categorie_id=3)
    sv.save()

    sv = Service(libelle="Réparation d'un équipement informatique", categorie_id=4)
    sv.save()

    ########### ETAT
    e = EtatDemande(libelle="Envoyée")
    e.save()

    e = EtatDemande(libelle="En cours")
    e.save()

    e = EtatDemande(libelle="Terminée")
    e.save()

    e = EtatDemande(libelle="Approuvée")
    e.save()

    e = EtatDemande(libelle="Archivée")
    e.save()
