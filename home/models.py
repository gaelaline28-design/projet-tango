from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.images.models import Image


# ---------------------------------------------------------------------------
# Snippet : Soirée / Événement
# ---------------------------------------------------------------------------

@register_snippet
class Soiree(models.Model):
    """Une soirée ou un stage affiché sur l'accueil et la page Soirées."""

    TYPE_CHOICES = [
        ('soiree', 'Soirée'),
        ('stage', 'Stage'),
        ('evenement', 'Événement'),
    ]

    type_evenement = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='soiree',
        verbose_name='Type',
    )
    titre = models.CharField(max_length=200, verbose_name='Titre')
    date = models.DateField(verbose_name='Date')
    lieu = models.CharField(max_length=200, verbose_name='Lieu')
    description = RichTextField(blank=True, verbose_name='Description')
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Image',
    )

    panels = [
        FieldPanel('type_evenement'),
        FieldPanel('titre'),
        FieldPanel('date'),
        FieldPanel('lieu'),
        FieldPanel('description'),
        FieldPanel('image'),
    ]

    class Meta:
        verbose_name = 'Soirée / Événement'
        verbose_name_plural = 'Soirées / Événements'
        ordering = ['date']

    def __str__(self):
        return f"{self.date} — {self.titre}"

    def get_type_label(self):
        return dict(self.TYPE_CHOICES).get(self.type_evenement, '')


# ---------------------------------------------------------------------------
# Page : Accueil
# ---------------------------------------------------------------------------

class HomePage(Page):
    """Page d'accueil du site."""

    # Texte de présentation
    texte_presentation = RichTextField(
        blank=True,
        verbose_name='Texte de présentation',
    )
    # Photo principale (photo des professeurs)
    photo_principale = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Photo des professeurs',
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('photo_principale'),
            FieldPanel('texte_presentation'),
        ], heading='Présentation'),
    ]

    class Meta:
        verbose_name = 'Page d\'accueil'

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Les deux prochaines soirées/événements
        from datetime import date
        context['soirees'] = Soiree.objects.filter(
            date__gte=date.today()
        ).order_by('date')[:2]
        return context
