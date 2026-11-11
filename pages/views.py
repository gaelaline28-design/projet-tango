from django.shortcuts import render

# redirect() = "envoie l'utilisateur vers une autre adresse"
from django.shortcuts import redirect

# send_mail() = envoie un e-mail (configuré dans settings.py)
from django.core.mail import send_mail
# send_mail() = envoie un e-mail (configuré dans settings.py)

# settings = les réglages du projet (EMAIL_HOST, CONTACT_EMAIL…)
from django.conf import settings
# settings = les réglages du projet (EMAIL_HOST, CONTACT_EMAIL…)

# @require_POST = "cette fonction n'accepte que les soumissions de formulaire"
# Si quelqu'un tape l'URL directement dans le navigateur → erreur 405
from django.views.decorators.http import require_POST



@require_POST
def contact_envoyer(request):

    # --- Lecture des données du formulaire ---
    # request.POST = dictionnaire des valeurs envoyées par le formulaire
    # .get('nom', '') = "donne-moi 'nom', ou '' si absent" → évite une erreur
    # .strip()        = supprime les espaces en début/fin de chaîne
    nom       = request.POST.get('nom',       '').strip()
    prenom    = request.POST.get('prenom',    '').strip()
    telephone = request.POST.get('telephone', '').strip()
    email     = request.POST.get('email',     '').strip()
    lieu      = request.POST.get('lieu',      '').strip()
    message   = request.POST.get('message',   '').strip()
    motif     = request.POST.get('motif',     'inscription')
    rgpd      = request.POST.get('rgpd',      '')  # 'on' si coché, '' si non coché

    # --- Vérification des champs obligatoires ---
    # Même si le JavaScript vérifie côté navigateur,
    # on vérifie aussi ici côté serveur (sécurité indispensable).
    erreurs = []

    if not nom:
        erreurs.append("Le nom est obligatoire.")

    if not email or '@' not in email:
        erreurs.append("L'adresse e-mail est invalide.")

    if not rgpd:
        erreurs.append("Vous devez accepter la politique RGPD.")

    # S'il y a des erreurs → retour au formulaire avec un signal d'erreur
    if erreurs:
        return redirect('/contact/?erreur=1')

    # --- Construction du texte de l'e-mail ---
    motif_texte = "S'inscrire" if motif == 'inscription' else "Poser une question"

    # f"..." = f-string : les {variables} entre accolades sont remplacées par leur valeur
    sujet = f"[El Firulete] Nouveau message de {prenom} {nom}"

    corps = f"""
Nouveau message reçu via le site El Firulete
=============================================
Motif      : {motif_texte}
Nom        : {nom}
Prénom     : {prenom}
Téléphone  : {telephone if telephone else 'Non renseigné'}
E-mail     : {email}
Lieu/cours : {lieu if lieu else 'Non renseigné'}

Message :
---------
{message if message else '(aucun message)'}
=============================================
    """.strip()

    # --- Envoi de l'e-mail ---
    try:
        # try = "essaie ce bloc ; si ça plante, passe au except"
        send_mail(
            subject=sujet,
            message=corps,
            from_email=settings.DEFAULT_FROM_EMAIL,  # expéditeur (dans settings.py)
            recipient_list=[settings.CONTACT_EMAIL],  # destinataire (dans settings.py)
            fail_silently=False,
        )
    except Exception as e:
        # En cas d'erreur d'envoi : on affiche dans la console (ne bloque pas l'user)
        print(f"Erreur envoi e-mail : {e}")

    # --- Redirection vers la page de confirmation ---
    # On ajoute le lieu dans l'URL pour l'afficher sur la page "Merci"
    return redirect(f'/contact/merci/?lieu={lieu}')