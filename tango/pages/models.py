{% extends "base.html" %}
{% load wagtailcore_tags wagtailimages_tags %}

{% block title %}Histoire du tango et de la milonga — Tango argentin{% endblock %}

{% block content %}

#   <!-- ===================== EN-TÊTE DE PAGE ===================== -->
  <section class="page-hero">
    <div class="page-hero-inner">
      <h1>Histoire du tango et de la milonga</h1>
    </div>
  </section>

#   <!-- ===================== IMAGE / FRISE CHRONOLOGIQUE ===================== -->
  <section class="section-frise">
    <div class="section-inner">
      {% if page.image_frise %}
        {% image page.image_frise max-1100 as img_frise %}
        <img
          src="{{ img_frise.url }}"
          alt="Frise chronologique du tango"
          width="{{ img_frise.width }}"
          height="{{ img_frise.height }}"
          class="frise-img"
        >
      {% else %}
        <div class="frise-placeholder">Image / frise chronologique</div>
      {% endif %}
    </div>
  </section>

#   <!-- ===================== HISTOIRE DU TANGO + LA MILONGA ===================== -->
  <section class="section-textes">
    <div class="section-inner section-textes-inner">

      <div class="bloc-texte">
        <h2>Histoire du tango</h2>
        {% if page.texte_histoire %}
          <div class="texte-riche">{{ page.texte_histoire|richtext }}</div>
        {% else %}
          <p>Né à Buenos Aires à la fin du XIXe siècle, le tango est le fruit des migrations italiennes, espagnoles et africaines. D'abord dansé dans les conventillos des faubourgs, il conquiert peu à peu les salons et traverse l'Atlantique pour séduire l'Europe.</p>
        {% endif %}
      </div>

      <div class="bloc-texte">
        <h2>La milonga</h2>
        {% if page.texte_milonga %}
          <div class="texte-riche">{{ page.texte_milonga|richtext }}</div>
        {% else %}
          <p>La milonga désigne à la fois une danse et le bal de tango. Une soirée milonga s'organise en tandas (séries de morceaux d'un même style) séparées par des cortinas (courts intermèdes musicaux qui invitent à changer de partenaire).</p>
        {% endif %}
      </div>

    </div>
  </section>

#   <!-- ===================== LES 3 DANSES D'UNE MILONGA ===================== -->
  <section class="section-3danses">
    <div class="section-inner">
      <div class="bloc-3danses">
        <h2>Les 3 danses d'une milonga</h2>
        <div class="liens-danses">
          <a href="/les-danses/tango/" class="btn-danse">
            Tango
            <svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </a>
          <a href="/les-danses/valse/" class="btn-danse">
            Valse
            <svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </a>
          <a href="/les-danses/milonga/" class="btn-danse">
            Milonga
            <svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </a>
        </div>
      </div>
    </div>
  </section>

{% endblock %}
