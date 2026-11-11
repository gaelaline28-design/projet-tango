from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
 
 
# ============================================================
#  SNIPPETS — Contenus réutilisables gérés dans l'admin
# ============================================================
 
@register_snippet   # ce décorateur enregistre la classe comme Snippet Wagtail
class Soiree(models.Model):
    """
    Une soirée ou un stage.
    Affiché sur la page d'accueil (les 2 prochaines)
    et sur la page Soirées (toutes).
    Se gère dans Admin → Snippets → Soirées.
    """
 
    # Choix possibles pour le type d'événement
    TYPE_CHOICES = [
        ('soiree',    'Soirée'),
        ('stage',     'Stage'),
        ('evenement', 'Événement'),
    ]
 
    type_evenement = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,  # affiche une liste déroulante dans l'admin
        default='soiree',
        verbose_name='Type',
    )
    titre       = models.CharField(max_length=200, verbose_name='Titre')
    date        = models.DateField(verbose_name='Date')
    lieu        = models.CharField(max_length=200, verbose_name='Lieu')
    description = RichTextField(blank=True, verbose_name='Description')
    image       = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Image',
    )
 
    # panels = les champs affichés dans l'admin (snippets utilisent "panels")
    panels = [
        FieldPanel('type_evenement'),
        FieldPanel('titre'),
        FieldPanel('date'),
        FieldPanel('lieu'),
        FieldPanel('description'),
        FieldPanel('image'),
    ]
 
    class Meta:
        verbose_name        = 'Soirée / Événement'
        verbose_name_plural = 'Soirées / Événements'
        ordering            = ['date']   # triées par date dans l'admin
 
    def __str__(self):
        # __str__ = ce qui s'affiche dans la liste admin (ex : "2025-03-15 — Milonga")
        return f"{self.date} — {self.titre}"
 
    def get_type_label(self):
        # Renvoie le texte lisible du type (ex : 'soiree' → 'Soirée')
        return dict(self.TYPE_CHOICES).get(self.type_evenement, '')
 
 
@register_snippet
class Cours(models.Model):
    """
    Un lieu de cours avec son horaire et son niveau.
    Se gère dans Admin → Snippets → Cours.
    Utilisé sur la page Nos cours et dans le formulaire de contact.
    """
 
    NIVEAU_CHOICES = [
        ('debutant',      'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance',        'Avancé'),
        ('tous',          'Tous niveaux'),
    ]
 
    ville       = models.CharField(max_length=100, verbose_name='Ville / Lieu')
    jour_horaire = models.CharField(max_length=200, verbose_name='Jour et horaire')
    niveau      = models.CharField(
        max_length=20,
        choices=NIVEAU_CHOICES,
        default='tous',
        verbose_name='Niveau',
    )
    adresse     = models.CharField(max_length=300, verbose_name='Adresse')
    lien_plan   = models.URLField(
        blank=True,
        verbose_name='Lien plan (Google Maps)',
    )
 
    panels = [
        FieldPanel('ville'),
        FieldPanel('jour_horaire'),
        FieldPanel('niveau'),
        FieldPanel('adresse'),
        FieldPanel('lien_plan'),
    ]
 
    class Meta:
        verbose_name        = 'Cours'
        verbose_name_plural = 'Cours'
        ordering            = ['ville']
 
    def __str__(self):
        return f"{self.ville} — {self.jour_horaire}"
 
 
@register_snippet
class Tarif(models.Model):
    """
    Un tarif affiché sur la page Nos cours.
    Se gère dans Admin → Snippets → Tarifs.
    """
 
    libelle = models.CharField(max_length=200, verbose_name='Libellé')
    montant = models.CharField(max_length=50,  verbose_name='Montant (ex: 300 €/an)')
    ordre   = models.PositiveSmallIntegerField(default=0, verbose_name="Ordre d'affichage")
 
    panels = [
        FieldPanel('libelle'),
        FieldPanel('montant'),
        FieldPanel('ordre'),
    ]
 
    class Meta:
        verbose_name        = 'Tarif'
        verbose_name_plural = 'Tarifs'
        ordering            = ['ordre']
 
    def __str__(self):
        return f"{self.libelle} : {self.montant}"
 
 
# ============================================================
#  PAGES — Chaque classe = un type de page dans Wagtail
# ============================================================
 
class HistoriquePage(Page):
    """
    Page : Histoire du tango et de la milonga
    URL prévue : /histoire/
    Template   : pages/templates/pages/historique_page.html
    """
 
    image_frise    = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Image / frise chronologique',
    )
    texte_histoire = RichTextField(blank=True, verbose_name='Histoire du tango')
    texte_milonga  = RichTextField(blank=True, verbose_name='La milonga')
 
    content_panels = Page.content_panels + [
        FieldPanel('image_frise'),
        MultiFieldPanel([
            FieldPanel('texte_histoire'),
            FieldPanel('texte_milonga'),
        ], heading='Contenus texte'),
    ]
 
    class Meta:
        verbose_name = 'Page Histoire'
 
 
class LesDansesPage(Page):
    """
    Page : Les danses (liste des 3 danses)
    URL prévue : /les-danses/
    Template   : pages/templates/pages/les_danses_page.html
 
    Les pages Tango, Valse, Milonga sont des pages ENFANTS de celle-ci
    dans l'arborescence Wagtail.
    get_context() les récupère automatiquement.
    """
 
    intro = RichTextField(blank=True, verbose_name="Texte d'introduction")
 
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
 
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Récupère les pages enfants de type DansePage, publiées, triées par titre
        context['danses'] = DansePage.objects.child_of(self).live().order_by('title')
        return context
 
    class Meta:
        verbose_name = 'Page Les danses'
 
 
class DansePage(Page):
    """
    Page : Détail d'une danse (Tango, Valse ou Milonga)
    URL prévue : /les-danses/tango/  (ou valse, milonga)
    Template   : pages/templates/pages/danse_page.html
 
    Ces pages sont des ENFANTS de LesDansesPage dans l'arborescence.
    """
 
    image      = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Image de la danse',
    )
    texte      = RichTextField(blank=True, verbose_name='Texte de présentation')
    url_youtube = models.URLField(
        blank=True,
        verbose_name='URL vidéo YouTube',
        help_text='Exemple : https://www.youtube.com/watch?v=XXXXXXXXX',
    )
 
    content_panels = Page.content_panels + [
        FieldPanel('image'),
        FieldPanel('texte'),
        FieldPanel('url_youtube'),
    ]
 
    def get_youtube_embed(self):
        """
        Transforme une URL YouTube normale en URL d'intégration iframe.
        Exemple :
          https://www.youtube.com/watch?v=AbCdEfGhIjK
          →  https://www.youtube.com/embed/AbCdEfGhIjK
        """
        import re
        url = self.url_youtube
        if not url:
            return ''
        # re.search cherche un motif dans la chaîne
        # Le motif : "v=" ou "youtu.be/" suivi de 11 caractères (l'ID de la vidéo)
        match = re.search(r'(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})', url)
        if match:
            return f"https://www.youtube.com/embed/{match.group(1)}"
        return ''
 
    class Meta:
        verbose_name        = 'Page Danse'
        verbose_name_plural = 'Pages Danses'
 
 
class ProfesseursPage(Page):
    """
    Page : Les professeurs (Julia, Andres + l'association)
    URL prévue : /professeurs/
    Template   : pages/templates/pages/professeurs_page.html
    """
 
    # --- Julia ---
    nom_julia   = models.CharField(max_length=100, default='Julia', verbose_name='Prénom')
    photo_julia = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Photo',
    )
    bio_julia   = RichTextField(blank=True, verbose_name='Biographie')
 
    # --- Andres ---
    nom_andres   = models.CharField(max_length=100, default='Andres', verbose_name='Prénom')
    photo_andres = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Photo',
    )
    bio_andres   = RichTextField(blank=True, verbose_name='Biographie')
 
    # --- Association ---
    texte_asso  = RichTextField(blank=True, verbose_name="Texte L'association El Firulete")
    photo_groupe = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Photo du groupe',
    )
 
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('nom_julia'),
            FieldPanel('photo_julia'),
            FieldPanel('bio_julia'),
        ], heading='Julia'),
        MultiFieldPanel([
            FieldPanel('nom_andres'),
            FieldPanel('photo_andres'),
            FieldPanel('bio_andres'),
        ], heading='Andres'),
        MultiFieldPanel([
            FieldPanel('texte_asso'),
            FieldPanel('photo_groupe'),
        ], heading="L'association El Firulete"),
    ]
 
    class Meta:
        verbose_name = 'Page Professeurs'
 
 
class NosCoursPage(Page):
    """
    Page : Nos cours (lieux + tarifs)
    URL prévue : /nos-cours/
    Template   : pages/templates/pages/nos_cours_page.html
 
    Les données (lieux, tarifs) sont dans les Snippets Cours et Tarif.
    get_context() les passe au template.
    """
 
    content_panels = Page.content_panels
 
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['cours']  = Cours.objects.all()   # tous les lieux de cours
        context['tarifs'] = Tarif.objects.all()   # tous les tarifs
        return context
 
    class Meta:
        verbose_name = 'Page Nos cours'
 
 
class SoireesPage(Page):
    """
    Page : Soirées et événements (liste complète)
    URL prévue : /soirees/
    Template   : pages/templates/pages/soirees_page.html
    """
 
    content_panels = Page.content_panels
 
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        from datetime import date
        # Uniquement les soirées à venir, triées par date
        context['soirees'] = Soiree.objects.filter(
            date__gte=date.today()
        ).order_by('date')
        return context
 
    class Meta:
        verbose_name = 'Page Soirées'
 
 
class ContactPage(Page):
    """
    Page : Contact et inscription (formulaire)
    URL prévue : /contact/
    Template   : pages/templates/pages/contact_page.html
 
    Le formulaire est AFFICHÉ par cette page Wagtail.
    Mais quand on SOUMET le formulaire, c'est views.py qui traite les données.
    """
 
    content_panels = Page.content_panels
 
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # On passe la liste des lieux pour le menu déroulant du formulaire
        context['cours'] = Cours.objects.all()
        return context
 
    class Meta:
        verbose_name = 'Page Contact et inscription'
 