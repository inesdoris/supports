from django.shortcuts import render, redirect
from .models import *

def index(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    demandes = Demande.objects.filter(etat__libelle="Affectée").filter(agent=user)
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

def mettre_en_traitement(request, id_demande):
    user_id = request.session.get('user_id', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    try:
        demande = Demande.objects.get(id=id_demande)
        if demande.agent==user:
            demande.etat = EtatDemande.objects.get(libelle="En cours")
            demande.save()
            request.session["success"] = f"La demande n°{demande.id} a été mise en cours de traitement"
        else:
            raise("error")
    except:
        request.session["error"] = f"Echec de mise en traitement de la demande n°{demande.id}"
    if not demande.service.categorie:
        request.session["error"] = f"La mise en traitement d'une demande est tributaire à sa catégorisation. Veuillez donc d'abord catégoriser la demande n°{demande.id}"
    else:
        return redirect("/agent/pending")
    return redirect("/agent")

def traiter_demande(request, id_demande):
    user_id = request.session.get('user_id', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    services = Service.objects.exclude(libelle="...")
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    demande = Demande.objects.get(id=id_demande)
    if demande.agent==user:
        if request.method == "POST":
            solution = request.POST.get("solution_detaillee")
            service_apporte = request.POST.get("service_apporte")
            if solution and id_demande and Service.objects.get(libelle=service_apporte):
                try:
                    # modififcation de l'état de la demande

                    demande.service.libelle = service_apporte
                    demande.etat = EtatDemande.objects.get(libelle="Terminée")
                    demande.save()
                    # enregistrement de la solution
                    solution = Traiter.objects.create(demande=demande, utilisateur=user, solution=solution)
                    request.session["success"] = f"La demande {id_demande} a été traitée avec succès."
                except:
                    request.session["error"] = f"La demande {id_demande} n'a pas pu être traitée."
                return redirect("/agent/solved")
    return render(request, "agent/traiter_demande.html", {
        "user": user,
        "services": services,
        "description_demande": demande.description,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })

def consulter_demande(request, id_demande):
    user_id = request.session.get('user_id', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    if id_demande:
        try:
            traitement = Traiter.objects.filter(demande=Demande.objects.get(id=id_demande))
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
    if request.method == "POST":
        try:
            categorie = CategorieService.objects.get(request.POST.get("categorie_choisie"))
            demande = Demande.objects.get(id=id_demande)
            demande.service = Service.objects.create(libelle="...", categorie=categorie)
            demande.save()
        except:
            return redirect("/agent")
    return render(request, "agent/categoriser_demande.html", {
        "user": user,
        "categories": categories,
        "description_demande": demande.description,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })
