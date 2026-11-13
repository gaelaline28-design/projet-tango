from django.conf import settings
from django.urls import include, path
from django.contrib import admin

# Nos vues manuelles (seulement le formulaire de contact)
from pages.views import contact_envoyer

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.views.generic import TemplateView

# from search import views as search_views

# Vue simple pour la page "Merci" après le formulaire
from django.shortcuts import render

def contact_merci(request):

    # permet d'afficher la page de confirmation après l'envoi du formulaire.
    # C'est une vue très simple : elle affiche juste le template.

    return render(request, 'pages/contact_merci.html')



urlpatterns = [
    
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),

    # path("search/", search_views.search, name="search"),

    #  Traitement du formulaire de contact
    #   → appelé quand l'utilisateur clique "Envoyer"
    #   → gère la lecture des données + envoi e-mail
    path('contact/envoyer/', contact_envoyer, name='contact_envoyer'),

    # Page de confirmation après envoi du formulaire
    path('contact/merci/', contact_merci, name='contact_merci'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
