from django.shortcuts import render, redirect
from .models import *


# Create your views here.
def index(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'index.html', {
        "error":error,
        "success":success,
        "user":user,
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
        "success":success,
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
    user =  Utilisateur.objects.get(id=user_id)
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
        "user":user,
        "error":error,
        "success":success,
    })
    

def ajout_utilisateur(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user =  Utilisateur.objects.get(id=user_id)
    profils=Profil.objects.all()
    agences=Agence.objects.all()
    sections=Section.objects.all()
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
        u = Utilisateur(login=username, password=chiffrement(password), nom=nom, prenom=prenom, email=email, sexe=sexe, adresse=adresse, contact=contact,  
                        profil_id=int(profil), agence_id=int(agence), image=image)
        if section:
            u.section = Section.objects.get(id=int(section))
        u.save()
        request.session["success"] = "L'utilisateur a été enregistré avec succès !!"
        return redirect("/utilisateur/liste")

    return render(request, "utilisateur/ajout.html",{
        "error":error,
        "success":success,
        "user":user,
        "profils":profils,
        "agences":agences,
        "sections":sections
    })

def liste_utilisateur(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user =  Utilisateur.objects.get(id=user_id)
    utilisateurs = Utilisateur.objects.all()
    return render(request, "utilisateur/liste.html",{
        "error":error,
        "success":success,
        "user":user,
        "utilisateurs":utilisateurs
    })

def modifier_utilisateur(request, id):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user =  Utilisateur.objects.get(id=user_id)
    profils=Profil.objects.all()
    agences=Agence.objects.all()
    sections=Section.objects.all()
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
    return render(request, "utilisateur/modifier.html",{
        "error":error,
        "success":success,
        "user":user,
        "u":u,
        "profils":profils,
        "agences":agences,
        "sections":sections
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
    user =  Agence.objects.get(id=user_id)
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

    return render(request, "agence/ajout.html",{
        "error":error,
        "success":success,
        "user":user
    })

def liste_agence(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user =  Agence.objects.get(id=user_id)
    agences = Agence.objects.all()
    return render(request, "agence/liste.html",{
        "error":error,
        "success":success,
        "user":user,
        "agences":agences
    })

def modifier_agence(request, id):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user =  Agence.objects.get(id=user_id)
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
    return render(request, "agence/modifier.html",{
        "error":error,
        "success":success,
        "user":user,
        "a":a
    })

def supprimer_agence(request, id):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user =  Agence.objects.get(id=user_id)
    a = Agence.objects.get(id=id)
    if request.POST:
        nom = request.POST.get("nom")
        #contact = request.POST.get("contact")
        try:
            a.nom = nom
            #a.contact = contact
        except:
            request.session["error"] = "La suppression ne s'est pas bien déroulée"
            return redirect(f"/agence/{a.id}/supprimer")
        a.save()
        request.session["success"] = "La suppression s'est bien déroulée"
        return redirect("/agence/liste")
    return render(request, "agence/supprimer.html",{
        "error":error,
        "success":success,
        "user":user,
        "a":a
    })

def formulaire(request):
    user_id = request.session.get('user_id', None)
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    if not user_id:
        return redirect('/login')
    user =  Utilisateur.objects.get(id=user_id)
    demandeur=Utilisateur.objects.all()
    service=Service.objects.all()
    if request.POST:
        description = request.POST.get("description")
        etat = request.POST.get("etat")
        demandeur = request.POST.get("demandeur")
        service = request.POST.get("service")
        date_formulation = request.POST.get("datef")
        d = Demande(description=description, etat=etat, demandeur=demandeur, service=service, date_formulation=date_formulation)
        d.save()
        request.session["success"] = "La demande a bien été envoyée !!"
        return redirect("/chef_agence/formulaire")

    return render(request, "chef_agence/formulaire.html",{
        "error":error,
        "success":success,
        "user":user,
        "demandeur":demandeur,
        "service":service
    })