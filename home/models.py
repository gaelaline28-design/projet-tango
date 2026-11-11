from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel



# ---------------------------------------------------------------------------
# Page : Accueil
# ---------------------------------------------------------------------------

class HomePage(Page):
    """Page d'accueil du site."""

    # Photo principale (photo des professeurs) :
    photo_principale = models.ForeignKey(
        'wagtailimages.Image',      # pointe vers les images gérées par Wagtail
        null=True,                  # peut être vide en base de données
        blank=True,                 # peut être vide dans le formulaire admin
        on_delete=models.SET_NULL,  # si l'image est supprimée → met NULL
        related_name='+',           
        verbose_name='Photo des professeurs',
    )
    
    # Texte de présentation
    texte_presentation = RichTextField(
        blank=True,
        verbose_name='Texte de présentation',
    )

    # --- Panneaux affichés dans l'interface d'administration Wagtail ---
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('photo_principale'),
            FieldPanel('texte_presentation'),
        ], 
        heading='Présentation'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # On importe Soiree depuis l'application "pages"
        from pages.models import Soiree
        from datetime import date

        # filtre : uniquement les soirées dont la date >= aujourd'hui
        context['soirees'] = Soiree.objects.filter(
            date__gte=date.today()
        ) .order_by('date')[:2]
        # order by : les plus proches d'abord
        # [:2]      : on prend seulement les 2 premières
        
        return context
 
    class Meta:
        verbose_name = "Page d'accueil"
