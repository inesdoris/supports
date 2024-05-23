from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *
from .forms import AffectationAgentForm, DemandeForm


# Create your views here.
def index(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)

    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    if user.profil == Profil.objects.get(id=1):
        return redirect("/demande/recues")
    if user.profil == Profil.objects.get(id=2):
        return redirect("/agent")
    if user.profil == Profil.objects.get(id=3):
        return redirect("chef_agence/dashboard")
    return render(request, 'index.html', {
        "error": error,
        "success": success,
        "user": user,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })


def login(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if user_id:
        return redirect('/')
    if request.POST:
        login = request.POST['login']
        password = request.POST['password']
        if Utilisateur.objects.filter(login=login).exists():
            u = Utilisateur.objects.filter(login=login).first()
            if u.password == chiffrement(password):
                request.session["user_id"] = u.id
                return redirect("/")
            else:
                request.session["error"] = "Login ou mot de passe incorrect"
                return redirect('/login')
        else:
            request.session["error"] = "Login ou mot de passe incorrect"
            return redirect('/login')
    return render(request, 'login.html', {
        "error": error,
        "success": success,
    })


def logout(request):
    del request.session['user_id']
    return redirect('/')


def profil(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    if request.POST:
        if "photo" in request.FILES:
            user.image = request.FILES["photo"]
            user.save()
            return redirect("/profil")
        if "currentPassword" in request.POST:
            currentPassword = request.POST["currentPassword"]
            if user.password == chiffrement(currentPassword):
                newPassword = request.POST["newPassword"]
                renewPassword = request.POST["renewPassword"]
                if newPassword == renewPassword:
                    user.password = chiffrement(newPassword)
                    user.save()
                    success = "Mot de passe modifié avec succès"
                    request.session["success"] = success
                    return redirect("/profil")
                else:
                    error = "Les mots de passe ne correspondent pas"
                    request.session["error"] = error
                    return redirect("/profil")
            else:
                error = "Mot de passe actuel incorrect"
                request.session["error"] = error
                return redirect("/profil")

    return render(request, 'profil.html', {
        "user": user,
        "error": error,
        "success": success,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })


def ajout_utilisateur(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    profils = Profil.objects.all()
    agences = Agence.objects.all()
    sections = Section.objects.all()
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        email = request.POST.get("email")
        sexe = bool(int(request.POST.get("sexe")))
        adresse = request.POST.get("adresse")
        contact = request.POST.get("contact")
        profil = request.POST.get("profil")
        agence = request.POST.get("agence")
        section = request.POST.get("section")
        image = request.FILES.get("image")
        
        if Utilisateur.objects.filter(login=username).exists():
            error = "Ce nom d'utilisateur est déjà utilisé !!"
            request.session["error"] = error
            return redirect("/utilisateur/ajout")
        
        u = Utilisateur(
            login=username,
            password=chiffrement(password),
            nom=nom,
            prenom=prenom,
            email=email,
            sexe=sexe,
            adresse=adresse,
            contact=contact,
            profil_id=int(profil)
        )
        
        if image:
            u.image = image
        
        if agence:
            try:
                u.agence_id = int(agence)
            except ValueError:
                error = "Agence non valide"
                request.session["error"] = error
                return redirect("/utilisateur/ajout")
        
        if section:
            try:
                u.section_id = int(section)
            except ValueError:
                error = "Section non valide"
                request.session["error"] = error
                return redirect("/utilisateur/ajout")
        
        u.save()
        
        request.session["success"] = "L'utilisateur a été enregistré avec succès !!"
        return redirect("/utilisateur/liste")
    
    return render(request, "utilisateur/ajout.html", {
        "error": error,
        "success": success,
        "user": user,
        "profils": profils,
        "agences": agences,
        "sections": sections,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })



def liste_utilisateur(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    utilisateurs = Utilisateur.objects.all()
    return render(request, "utilisateur/liste.html", {
        "error": error,
        "success": success,
        "user": user,
        "utilisateurs": utilisateurs,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })


def modifier_utilisateur(request, id):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    profils = Profil.objects.all()
    agences = Agence.objects.all()
    sections = Section.objects.all()
    u = Utilisateur.objects.get(id=id)
    if request.POST:
        password = request.POST.get("password")
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        email = request.POST.get("email")
        sexe = bool(int(request.POST.get("sexe")))
        adresse = request.POST.get("adresse")
        contact = request.POST.get("contact")
        profil = request.POST.get("profil")
        agence = request.POST.get("agence")
        section = request.POST.get("section")

        image = request.FILES.get("image")
        try:
            u.password = chiffrement(password)
            u.nom = nom
            u.prenom = prenom
            u.email = email
            u.sexe = sexe
            u.adresse = adresse
            u.contact = contact
            u.profil = Profil.objects.get(id=int(profil))
            u.agence = Agence.objects.get(id=int(agence))
            if section:
                u.section = Section.objects.get(id=int(section))
            if image:
                u.image = image
        except:
            request.session["error"] = "La modification ne s'est pas bien déroulée"
            return redirect(f"/utilisateur/{u.id}/modifier")
        u.save()
        request.session["success"] = "La modification s'est bien déroulée"
        return redirect("/utilisateur/liste")
    return render(request, "utilisateur/modifier.html", {
        "error": error,
        "success": success,
        "user": user,
        "u": u,
        "profils": profils,
        "agences": agences,
        "sections": sections,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })


def supprimer_utilisateur(request, id):
    u = Utilisateur.objects.get(id=id)
    u.delete()
    request.session["success"] = "L'utilisateur a bien été supprimé !!"
    return redirect("/utilisateur/liste")


def ajout_agence(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    if request.POST:
        nom = request.POST.get("nom")
        if Agence.objects.filter(nom=nom).exists():
            error = "Ce nom d'agence existe déjà !!"
            request.session["error"] = error
            return redirect("/agence/ajout")
        a = Agence(nom=nom)
        a.save()
        request.session["success"] = "L'agence a été enregistrée avec succès !!"
        return redirect("/agence/liste")

    return render(request, "agence/ajout.html", {
        "error": error,
        "success": success,
        "user": user,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })


def liste_agence(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    agences = Agence.objects.all()
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    return render(request, "agence/liste.html", {
        "error": error,
        "success": success,
        "user": user,
        "agences": agences,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })


def modifier_agence(request, id):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    a = Agence.objects.get(id=id)
    if request.POST:
        nom = request.POST.get("nom")
        try:
            a.nom = nom
        except:
            request.session["error"] = "La modification ne s'est pas bien déroulée"
            return redirect(f"/agence/{a.id}/modifier")
        a.save()
        request.session["success"] = "La modification s'est bien déroulée"
        return redirect("/agence/liste")
    return render(request, "agence/modifier.html", {
        "error": error,
        "success": success,
        "user": user,
        "a": a,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })


def supprimer_agence(request, id):
    a = Agence.objects.get(id=id)
    a.delete()
    request.session["success"] = "L'agence a bien été supprimée !!"
    return redirect("/agence/liste")


def formulaire(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    demandeur = user
    service = Service.objects.all()
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    if request.POST:
        try:
            if request.POST.get('description') != "":
                description = request.POST.get("description")
            etat = EtatDemande.objects.get(id=1)
            demandeur = user
            service = Service.objects.get(id=request.POST.get("service"))
            service.categorie = None
            service.save()
            date_formulation = timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone())
            d = Demande(description=description, etat=etat, demandeur=demandeur, service=service,
                        date_formulation=date_formulation)
            d.save()
            nouvelle_notification = Notifications(
                receiver=Utilisateur.objects.get(profil__id=1),
                message="Vous avez reçue une nouvelle demande !",
                date_notification=timezone.localtime(timezone.now(), timezone=timezone.get_current_timezone()),
            )
            nouvelle_notification.save()
            request.session["success"] = "La demande a bien été envoyée !!"
            return redirect("/chef_agence/dashboard")

        except:
            request.session["error"] = "Une erreur est survenue"
            return redirect("/chef_agence/formulaire")

    return render(request, "chef_agence/formulaire.html", {
        "error": error,
        "success": success,
        "user": user,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications,
        "demandeur": demandeur,
        "service": service,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })
    
def liste_demandes_recues(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    demandes_recues = Demande.objects.filter(etat=EtatDemande.objects.get(libelle="Envoyée"))
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    return render(request, "demande/recues.html", {
        "error": error,
        "success": success,
        "user": user,
        "demandes_recues": demandes_recues,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })
    
def liste_demandes_affectees(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    demandes_affectees = Demande.objects.filter(etat=EtatDemande.objects.get(libelle="En cours"))
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    return render(request, "demande/affectees.html", {
        "error": error,
        "success": success,
        "user": user,
        "demandes_affectees": demandes_affectees,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })
    
def liste_demandes_traitees(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    
    user = Utilisateur.objects.get(id=user_id)
    demandes_traitees = Demande.objects.filter(etat=EtatDemande.objects.get(libelle="Approuvée"))
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    
    return render(request, "demande/traitees.html", {
        "error": error,
        "success": success,
        "user": user,
        "demandes_traitees": demandes_traitees,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })
    
def liste_demandes_envoyees_chef(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    
    user = Utilisateur.objects.get(id=user_id)
    demandes_traitees = Demande.objects.filter(etat=EtatDemande.objects.get(libelle="Archivée"))
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    
    return render(request, "demande/envoyer_chef.html", {
        "error": error,
        "success": success,
        "user": user,
        "demandes_traitees": demandes_traitees,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })

def envoyer_solution(request, demande_id):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    user = Utilisateur.objects.get(id=user_id)
    demande = Demande.objects.get(id=demande_id)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    traitement = Traiter.objects.filter(demande=demande).first()

    if request.method == 'POST':
        if traitement:
            demande.etat = EtatDemande.objects.get_or_create(libelle="Archivée")[0]
            demande.save()
            Notifications.objects.create(receiver=demande.demandeur, message=f"La solution à la demande [{demande.description}] vous a été envoyée par l'admin")
            request.session["success"] = "La solution a été envoyée avec succès"
            return redirect("/demande/traitees")

    return render(request, "demande/envoyer_solution.html", {
        "error": error,
        "success": success,
        "user": user,
        "demande": demande,
        "traitement": traitement,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })  
    
def affecter_agent(request, demande_id):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    user = Utilisateur.objects.get(id=user_id)
    demande = get_object_or_404(Demande, id=demande_id)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    if request.method == 'POST':
        try:
            form = AffectationAgentForm(request.POST, instance=demande)
            if form.is_valid():
                print(form.cleaned_data)
                form.save()
                Notifications.objects.create(receiver=form.cleaned_data['agent'], message="Une nouvelle demande vous a été affectée")
                return redirect('liste_demandes_recues')
        except:
            request.session["error"] = "Selectionner un agent"
            return redirect(f"/demande/{demande_id}/affecter_agent")
    else:
        form = AffectationAgentForm(instance=demande)
    return render(request, 'demande/affecter_agent.html', {
        "error": error,
        "success": success,
        "user": user,
        'form': form, 
        'demande': demande, 
        'nombre_nouvelles_notifications': nombre_nouvelles_notifications
        })

def chef_agence_dashboard(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)

    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    demandes = Demande.objects.filter(demandeur=user, etat=EtatDemande.objects.get(id=1)).order_by('-date_formulation')
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    return render(request, "chef_agence/dashboard.html", {
        "error": error,
        "success": success,
        "user": user,
        "demandes": demandes,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
    })

def chef_agence_demandes_en_attente(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    demandes_en_attente = Demande.objects.filter(demandeur=user, etat=EtatDemande.objects.get(id=2)).order_by('-date_formulation')

    return render(request, "chef_agence/demandes_en_attente.html", {
        "error": error,
        "success": success,
        "user": user,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications,
        "demandes_en_attente": demandes_en_attente
    })

def chef_agence_demandes_resolues(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    demandes_resolues = Traiter.objects.filter(demande__demandeur=user, demande__etat=EtatDemande.objects.get(id=5))

    return render(request, "chef_agence/demandes_resolues.html", {
        "error": error,
        "success": success,
        "user": user,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications,
        "demandes_resolues": demandes_resolues
    })

def consulter_demande(request, id):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    d = Demande.objects.get(id=id)
    s = Traiter.objects.filter(demande=d)
    return render(request, "chef_agence/consulter.html", {
        "error": error,
        "success": success,
        "user": user,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications,
        "d": d,
        "s": s
    })
    
def modifier_demande(request, demande_id):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    demande = get_object_or_404(Demande, id=demande_id)
    nombre_nouvelles_notifications = Notifications.objects.filter(receiver=user).filter(is_read=False).count()
    
    if request.method == 'POST':
        form = DemandeForm(request.POST, instance=demande)
        if form.is_valid():
            form.save()
            return redirect('consulter_demande', id=demande.id)  # Redirige vers la page de consultation
    else:
        form = DemandeForm(instance=demande)

    return render(request, 'chef_agence/modifier_demande.html', {
        "error": error,
        "success": success,
        "user": user,
        'form': form, 
        'demande': demande,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications
        })

def supprimer_demande(request, id):
    d = Demande.objects.get(id=id)
    d.delete()
    request.session["success"] = "La demande a bien été supprimée !!"
    return redirect("/chef_agence/dashboard")

def notifications(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)

    if not user_id:
        return redirect('/login')

    user = Utilisateur.objects.get(id=user_id)

    # Récupérer les nouvelles notifications non lues
    nouvelles_notifications = Notifications.objects.filter(receiver=user, is_read=False).order_by('-date_notification')

    # Récupérer et afficher les anciennes notifications lues
    anciennes_notifications = Notifications.objects.filter(receiver=user, is_read=True).order_by('-date_notification')

    # Marquer les nouvelles notifications comme lues après les avoir récupérées
    for notification in nouvelles_notifications:
        notification.is_read = True
        notification.save()

    # Récupérer le nombre de nouvelles notifications non lues après les avoir marquées comme lues
    nombre_nouvelles_notifications = nouvelles_notifications.count()

    template_name = "notifications.html"

    if user.profil.id == 2:
        template_name = "agent/notifications.html"

    return render(request, template_name, {
        "error": error,
        "success": success,
        "user": user,
        "nombre_nouvelles_notifications": nombre_nouvelles_notifications,
        "anciennes_notifications": anciennes_notifications,
        "nouvelles_notifications": nouvelles_notifications
    })

def supprimer_notification(request, id):
    n = Notifications.objects.get(id=id)
    n.delete()
    request.session["success"] = "La notification a bien été supprimée !!"
    return redirect("/notifications")
