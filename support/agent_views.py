from django.shortcuts import render, redirect
from .models import *

def index(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    demandes = Demande.objects.filter(etat__libelle="Envoyée").filter(agent=user)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    return render(request, 'agent/demandes_affectees.html', {
        "user": user,
        "error": error,
        "success": success,
        "demandes": demandes,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })

def pending(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    demandes = Demande.objects.filter(etat__libelle="En cours").filter(agent=user)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    return render(request, 'agent/demandes_en_cours.html', {
        "user": user,
        "error": error,
        "success": success,
        "demandes": demandes,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })

def solved(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    demandes = Demande.objects.filter(etat__libelle="Terminée").filter(agent=user)
    return render(request, 'agent/demandes_traitees.html', {
        "user": user,
        "error": error,
        "success": success,
        "demandes": demandes,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })

def admin(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    traitements = Traiter.objects.filter(utilisateur=user).filter(demande__etat__libelle="Approuvée")
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    return render(request, 'agent/demandes_admin.html', {
        "user": user,
        "error": error,
        "success": success,
        "traitements": traitements,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })

def mettre_en_traitement(request, id_demande):
    user_id = request.session.get('user_id', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    try:
        demande = Demande.objects.get(id=id_demande)
        if demande.agent != user:
            raise("error")
        if demande.service.categorie :
            demande.etat = EtatDemande.objects.get(libelle="En cours")
            demande.save()
            request.session["success"] = f"La demande n°{demande.id} a été mise en cours de traitement"
            return redirect("/agent/pending")
        else:
            request.session["error"] = f"La mise en traitement d'une demande est tributaire à sa catégorisation. Veuillez donc d'abord catégoriser la demande n°{demande.id}"
    except:
        request.session["error"] = f"Echec de mise en traitement de la demande n°{demande.id}"
    return redirect("/agent")

def abolir_traitement(request, id_demande):
    user_id = request.session.get('user_id', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    try:
        demande = Demande.objects.get(id=id_demande)
        if demande.agent != user:
            raise("error")
        traitement = Traiter.objects.get(demande=demande) if Traiter.objects.filter(demande=demande) else None
        if traitement and traitement.solution :
            demande.etat = EtatDemande.objects.get(libelle="Terminée")
            demande.save()
            request.session["success"] = f"La demande n°{demande.id} a été mise en fin de traitement"
            return redirect("/agent/solved")
        else:
            request.session["error"] = f"La mise en fin traitement d'une demande est tributaire à son traitement. Veuillez donc renseigner la solution proposée à la demande n°{demande.id}"
    except:
        request.session["error"] = f"Echec de mise en fin traitement de la demande n°{demande.id}"
    return redirect("/agent/pending")

def traiter_demande(request, id_demande):
    user_id = request.session.get('user_id', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    services = Service.objects.exclude(libelle="...")
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    demande = Demande.objects.get(id=id_demande)
    solution_precedemment_renseignee = Traiter.objects.get(demande=demande).solution if Traiter.objects.filter(demande=demande) else None
    if demande.agent==user:
        if request.method == "POST":
            solution = request.POST.get("solution_detaillee")
            if solution and id_demande:
                try:
                    # enregistrement de la solution
                    traitement = Traiter.objects.get_or_create(demande=demande, utilisateur=user)[0]
                    traitement.solution = solution
                    traitement.save()
                    request.session["success"] = f"La solution à la demande {id_demande} a été appliquée avec succès."
                except:
                    request.session["error"] = f"La solution à la demande {id_demande} n'a pas pu être appliquée."
                return redirect("/agent/pending")
    return render(request, "agent/traiter_demande.html", {
        "user": user,
        "services": services,
        "description_demande": demande.description,
        "solution_existante": solution_precedemment_renseignee,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })

def consulter_demande(request, id_demande):
    user_id = request.session.get('user_id', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    traitement = None
    if id_demande:
        d = Demande.objects.get(id=id_demande)
        if d.agent != user:
            raise("error")
        try:
            traitement = Traiter.objects.get(demande=d)
        except:
            return redirect("/agent/solved")
    return render(request, "agent/consulter_demande.html", {
        "user": user,
        "solution_demande": traitement.solution,
        "description_demande": traitement.demande.description,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })

def categoriser_demande(request, id_demande):
    user_id = request.session.get('user_id', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    categories = CategorieService.objects.all()
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    try:
        demande = Demande.objects.get(id=id_demande)
        if demande.agent != user:
            raise("error")
        if request.method == "POST":
            categorie = CategorieService.objects.get(libelle=request.POST.get("categorie_choisie"))
            # on modifie le service de la demande
            service = demande.service
            service.categorie = categorie
            service.save()
            # et on assigne le nouveau service à la demande
            demande.service = service
            demande.save()
            request.session["success"] = f"La catégorie '{categorie.libelle}' a été assignée à la demande n°{id_demande}"
            request.session["error"] = ""
            return redirect("/agent")
    except:
        request.session["error"] = f"La catégorisation de la demande n°{id_demande} a échouée. Veuillez réessayer."
        request.session["success"] = ""
        return redirect("/agent")
    return render(request, "agent/categoriser_demande.html", {
        "user": user,
        "categories": categories,
        "description_demande": demande.description if demande else None,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })

def notifier_admin(request, id_demande):
    user_id = request.session.get('user_id', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    demande = Demande.objects.get(id=id_demande)
    try:
        if demande.agent != user:
            raise("error")
        demande.etat = EtatDemande.objects.get_or_create(libelle="Approuvée")[0]
        demande.save()
        Notifications.objects.create(receiver=Utilisateur.objects.filter(profil__id=1).first(), message=f"Une proposition de solution à l'une des demandes de {'M.' if demande.demandeur.sexe else 'Mme'} {demande.demandeur.nom} {demande.demandeur.prenom} vous a été envoyée par l'agent {user.nom} {user.prenom}.")
        request.session["success"] = "La solution a été envoyée avec succès."
        return redirect("/agent/admin")
    except:
        request.session["error"] = "L'envoi de la solution a échoué..."
    return render(request, "agent/demandes_admin.html", {
        "user": user,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })
