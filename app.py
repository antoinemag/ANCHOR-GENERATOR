#!/usr/bin/env python3
"""
Générateur de profil d'ancres - Version Web (Streamlit)
"""

import streamlit as st
import random
import csv
import json
import io
from urllib.parse import urlparse
from dataclasses import dataclass
from typing import Optional


# =============================================================================
# CONFIGURATION
# =============================================================================

DISTRIBUTION = {
    "marque": 35,
    "url_nue": 20,
    "generique": 20,
    "partielle": 15,
    "exacte": 5,
    "longue_traine": 5,
}

GENERIQUES = {
    "fr": [
        "cliquez ici", "cliquer ici", "en savoir plus", "voir le site", "lire la suite",
        "plus d'infos", "découvrir", "visiter", "sur ce site", "ici", "voir",
        "ce lien", "cette page", "voir ici", "consultez", "accéder", "consulter",
        "plus de détails", "lire l'article", "voir l'article", "accéder au site",
        "découvrez", "explorez", "visitez", "consultez le site", "rendez-vous ici",
        "jetez un œil", "allez voir", "c'est par ici", "direction le site",
        "tout est ici", "les infos ici", "les détails ici", "en détail ici",
        "cette ressource", "ce guide", "cet article", "cette source", "ce contenu",
        "la source", "le site officiel", "le site de référence", "la référence",
        "sur cette page", "à cette adresse", "via ce lien", "par ici",
        "suivez ce lien", "depuis ce site", "disponible ici", "accessible ici",
        "retrouvez tout ici", "toutes les infos", "le détail complet",
        "c'est ici", "c'est là", "juste ici", "par là", "le lien",
        "voir ça", "checker ça", "mater ça", "go", "let's go",
    ],
    "en": [
        "click here", "learn more", "read more", "visit website", "see more",
        "more info", "discover", "check this out", "this site", "here",
        "this link", "this page", "see here", "find out more", "view more",
        "visit site", "go to site", "access here", "get details", "full details",
        "explore", "check it out", "take a look", "have a look", "see for yourself",
        "dive in", "get started", "start here", "jump in", "discover more",
        "find out", "dig deeper", "explore more", "uncover", "reveal",
        "this resource", "this guide", "this article", "this source", "the source",
        "official site", "the reference", "main site", "home page", "landing page",
        "on this page", "at this address", "via this link", "through here",
        "follow this link", "from this site", "available here", "accessible here",
        "right here", "over here", "this way", "head here", "go here",
        "it's here", "just here", "the link", "see this", "peep this",
    ],
    "es": [
        "haz clic aquí", "saber más", "leer más", "visitar sitio", "ver más",
        "más información", "descubrir", "ver aquí", "este sitio", "aquí",
        "este enlace", "esta página", "ver más detalles", "acceder", "consultar",
        "explorar", "descubre", "visita", "mira aquí", "echa un vistazo",
        "ir al sitio", "accede aquí", "encuentra más", "conoce más",
        "la fuente", "este recurso", "esta guía", "el sitio oficial",
        "disponible aquí", "por aquí", "desde aquí", "todo aquí",
        "es aquí", "justo aquí", "el enlace", "míralo", "descúbrelo",
    ],
    "pt": [
        "clique aqui", "saiba mais", "leia mais", "visitar site", "ver mais",
        "mais informações", "descobrir", "ver aqui", "este site", "aqui",
        "este link", "esta página", "mais detalhes", "acessar", "consultar",
        "explorar", "descubra", "visite", "veja aqui", "dê uma olhada",
        "ir ao site", "acesse aqui", "encontre mais", "conheça mais",
        "a fonte", "este recurso", "este guia", "o site oficial",
        "disponível aqui", "por aqui", "daqui", "tudo aqui",
        "é aqui", "bem aqui", "o link", "confira", "descubra",
    ],
    "de": [
        "hier klicken", "mehr erfahren", "weiterlesen", "Webseite besuchen", "mehr sehen",
        "mehr Infos", "entdecken", "hier ansehen", "diese Seite", "hier",
        "dieser Link", "diese Seite", "mehr Details", "zugreifen", "nachschauen",
        "erkunden", "entdecke", "besuche", "schau hier", "wirf einen Blick",
        "zur Seite", "hier zugreifen", "mehr finden", "mehr kennenlernen",
        "die Quelle", "diese Ressource", "dieser Guide", "die offizielle Seite",
        "hier verfügbar", "hierher", "von hier", "alles hier",
        "es ist hier", "genau hier", "der Link", "schau mal", "check das",
    ],
    "it": [
        "clicca qui", "scopri di più", "leggi di più", "visita il sito", "vedi altro",
        "maggiori informazioni", "scoprire", "vedi qui", "questo sito", "qui",
        "questo link", "questa pagina", "più dettagli", "accedi", "consulta",
        "esplora", "scopri", "visita", "guarda qui", "dai un'occhiata",
        "vai al sito", "accedi qui", "trova di più", "conosci di più",
        "la fonte", "questa risorsa", "questa guida", "il sito ufficiale",
        "disponibile qui", "da qui", "tutto qui", "è qui", "proprio qui",
        "il link", "guardalo", "scoprilo", "eccolo",
    ],
}

TEMPLATES_PARTIELLES = {
    "fr": [
        "{kw} 2024", "{kw} 2025", "{kw} cette année", "{kw} du moment",
        "{kw} actuel", "{kw} aujourd'hui", "nouveau {kw}", "{kw} récent",
        "meilleur {kw}", "top {kw}", "{kw} fiable", "{kw} sécurisé",
        "{kw} de confiance", "{kw} recommandé", "{kw} populaire", "{kw} réputé",
        "excellent {kw}", "{kw} de qualité", "{kw} premium", "{kw} pro",
        "{kw} numéro 1", "{kw} n°1", "{kw} leader", "{kw} référence",
        "{kw} france", "{kw} français", "{kw} en france", "{kw} fr",
        "{kw} europe", "{kw} belgique", "{kw} suisse", "{kw} canada",
        "{kw} en ligne", "{kw} online", "{kw} sur internet", "{kw} web",
        "{kw} mobile", "{kw} application", "{kw} app",
        "{kw} gratuit", "{kw} bonus", "{kw} promo", "{kw} offre",
        "{kw} pas cher", "{kw} prix", "{kw} tarif", "code {kw}",
        "guide {kw}", "avis {kw}", "{kw} avis", "{kw} test", "test {kw}",
        "{kw} comparatif", "comparatif {kw}", "{kw} review", "{kw} analyse",
        "{kw} présentation", "{kw} découverte", "tout sur {kw}",
        "jouer {kw}", "essayer {kw}", "tester {kw}", "découvrir {kw}",
        "accéder {kw}", "utiliser {kw}", "profiter {kw}",
        "{kw} inscription", "{kw} connexion", "{kw} compte", "{kw} login",
        "s'inscrire {kw}", "créer compte {kw}", "{kw} officiel",
        "site {kw}", "plateforme {kw}", "{kw} légal", "{kw} autorisé",
    ],
    "en": [
        "{kw} 2024", "{kw} 2025", "{kw} this year", "{kw} latest",
        "{kw} current", "{kw} today", "new {kw}", "{kw} recent",
        "best {kw}", "top {kw}", "{kw} trusted", "{kw} safe",
        "{kw} reliable", "{kw} recommended", "{kw} popular", "{kw} reputable",
        "excellent {kw}", "{kw} quality", "{kw} premium", "{kw} pro",
        "{kw} number 1", "{kw} #1", "{kw} leading", "{kw} reference",
        "{kw} uk", "{kw} usa", "{kw} us", "{kw} canada",
        "{kw} australia", "{kw} europe", "{kw} worldwide", "{kw} international",
        "{kw} online", "{kw} web", "{kw} internet", "{kw} digital",
        "{kw} mobile", "{kw} app", "{kw} application",
        "free {kw}", "{kw} bonus", "{kw} promo", "{kw} deal",
        "cheap {kw}", "{kw} price", "{kw} cost", "{kw} code",
        "{kw} guide", "{kw} review", "review {kw}", "{kw} test", "test {kw}",
        "{kw} comparison", "compare {kw}", "{kw} analysis", "{kw} overview",
        "{kw} introduction", "{kw} discovery", "all about {kw}",
        "play {kw}", "try {kw}", "test {kw}", "discover {kw}",
        "access {kw}", "use {kw}", "enjoy {kw}",
        "{kw} signup", "{kw} login", "{kw} account", "{kw} register",
        "join {kw}", "create {kw} account", "{kw} official",
        "{kw} site", "{kw} platform", "{kw} legal", "{kw} licensed",
    ],
    "es": [
        "{kw} 2024", "{kw} 2025", "{kw} este año", "{kw} actual",
        "mejor {kw}", "top {kw}", "{kw} seguro", "{kw} fiable",
        "{kw} confiable", "{kw} recomendado", "{kw} popular",
        "{kw} españa", "{kw} mexico", "{kw} latino", "{kw} online",
        "{kw} gratis", "{kw} bono", "{kw} promoción", "código {kw}",
        "guía {kw}", "{kw} opiniones", "{kw} reseña", "{kw} análisis",
        "probar {kw}", "jugar {kw}", "acceder {kw}", "{kw} registro",
        "{kw} login", "sitio {kw}", "{kw} oficial", "{kw} legal",
        "{kw} comparativa", "todo sobre {kw}", "nuevo {kw}",
    ],
    "pt": [
        "{kw} 2024", "{kw} 2025", "{kw} este ano", "{kw} atual",
        "melhor {kw}", "top {kw}", "{kw} seguro", "{kw} confiável",
        "{kw} recomendado", "{kw} popular", "{kw} brasil", "{kw} portugal",
        "{kw} online", "{kw} grátis", "{kw} bônus", "{kw} promoção",
        "código {kw}", "guia {kw}", "{kw} avaliação", "{kw} análise",
        "testar {kw}", "jogar {kw}", "acessar {kw}", "{kw} cadastro",
        "{kw} login", "site {kw}", "{kw} oficial", "{kw} legal",
        "{kw} comparação", "tudo sobre {kw}", "novo {kw}",
    ],
    "de": [
        "{kw} 2024", "{kw} 2025", "{kw} dieses Jahr", "{kw} aktuell",
        "beste {kw}", "top {kw}", "{kw} sicher", "{kw} seriös",
        "{kw} zuverlässig", "{kw} empfohlen", "{kw} beliebt",
        "{kw} deutschland", "{kw} österreich", "{kw} schweiz", "{kw} online",
        "{kw} kostenlos", "{kw} bonus", "{kw} angebot", "{kw} code",
        "{kw} guide", "{kw} bewertung", "{kw} test", "{kw} analyse",
        "{kw} ausprobieren", "{kw} spielen", "{kw} zugreifen", "{kw} anmeldung",
        "{kw} login", "{kw} seite", "{kw} offiziell", "{kw} legal",
        "{kw} vergleich", "alles über {kw}", "neu {kw}",
    ],
    "it": [
        "{kw} 2024", "{kw} 2025", "{kw} quest'anno", "{kw} attuale",
        "migliore {kw}", "top {kw}", "{kw} sicuro", "{kw} affidabile",
        "{kw} consigliato", "{kw} popolare", "{kw} italia", "{kw} italiano",
        "{kw} online", "{kw} gratis", "{kw} bonus", "{kw} promozione",
        "codice {kw}", "guida {kw}", "{kw} recensione", "{kw} analisi",
        "provare {kw}", "giocare {kw}", "accedere {kw}", "{kw} registrazione",
        "{kw} login", "sito {kw}", "{kw} ufficiale", "{kw} legale",
        "{kw} confronto", "tutto su {kw}", "nuovo {kw}",
    ],
}

TEMPLATES_LONGUE_TRAINE = {
    "fr": [
        "comment {kw}", "comment utiliser {kw}", "comment accéder à {kw}",
        "comment s'inscrire sur {kw}", "comment fonctionne {kw}",
        "comment jouer sur {kw}", "comment profiter de {kw}",
        "comment commencer avec {kw}", "comment se connecter à {kw}",
        "où trouver {kw}", "où jouer {kw}", "où s'inscrire {kw}",
        "où accéder à {kw}", "où utiliser {kw}",
        "pourquoi {kw}", "pourquoi choisir {kw}", "pourquoi utiliser {kw}",
        "pourquoi s'inscrire sur {kw}", "pourquoi préférer {kw}",
        "quel {kw} choisir", "quelle est le meilleur {kw}",
        "quel est le top {kw}", "quels sont les avantages de {kw}",
        "est-ce que {kw} est fiable", "est-ce que {kw} est légal",
        "est-ce que {kw} est sécurisé", "est-ce que {kw} vaut le coup",
        "guide complet {kw}", "guide {kw} débutant", "guide {kw} 2024",
        "tutoriel {kw}", "tuto {kw}", "formation {kw}",
        "apprendre {kw}", "débuter avec {kw}", "se lancer sur {kw}",
        "les meilleurs {kw}", "top 10 {kw}", "classement {kw}",
        "liste des {kw}", "sélection {kw}", "comparatif {kw} 2024",
        "meilleur {kw} du moment", "{kw} vs concurrent",
        "avis sur {kw}", "avis {kw} 2024", "retour d'expérience {kw}",
        "mon avis sur {kw}", "que vaut {kw}", "test complet {kw}",
        "{kw} arnaque ou fiable", "{kw} vaut-il le coup",
        "tout savoir sur {kw}", "tout comprendre sur {kw}",
        "présentation de {kw}", "découverte de {kw}", "introduction à {kw}",
        "{kw} pour débutants", "{kw} pour les nuls", "{kw} expliqué",
        "bonus {kw} sans dépôt", "code promo {kw} 2024",
        "inscription {kw} gratuite", "offre de bienvenue {kw}",
        "{kw} avec bonus", "{kw} sans inscription",
    ],
    "en": [
        "how to {kw}", "how to use {kw}", "how to access {kw}",
        "how to sign up for {kw}", "how does {kw} work",
        "how to play on {kw}", "how to benefit from {kw}",
        "how to start with {kw}", "how to log in to {kw}",
        "where to find {kw}", "where to play {kw}", "where to sign up {kw}",
        "where to access {kw}", "where to use {kw}",
        "why {kw}", "why choose {kw}", "why use {kw}",
        "why sign up for {kw}", "why prefer {kw}",
        "which {kw} to choose", "what is the best {kw}",
        "what is the top {kw}", "what are the benefits of {kw}",
        "is {kw} legit", "is {kw} legal", "is {kw} safe", "is {kw} worth it",
        "is {kw} trustworthy", "is {kw} reliable",
        "complete {kw} guide", "{kw} beginner guide", "{kw} guide 2024",
        "{kw} tutorial", "{kw} walkthrough", "{kw} training",
        "learn {kw}", "getting started with {kw}", "start with {kw}",
        "the best {kw}", "top 10 {kw}", "{kw} ranking",
        "list of {kw}", "{kw} selection", "{kw} comparison 2024",
        "best {kw} right now", "{kw} vs competitors",
        "{kw} review", "{kw} review 2024", "{kw} experience",
        "my {kw} review", "is {kw} good", "full {kw} test",
        "{kw} scam or legit", "is {kw} worth it",
        "everything about {kw}", "understand {kw}",
        "{kw} overview", "{kw} discovery", "introduction to {kw}",
        "{kw} for beginners", "{kw} explained", "{kw} 101",
        "{kw} no deposit bonus", "{kw} promo code 2024",
        "free {kw} signup", "{kw} welcome offer",
        "{kw} with bonus", "{kw} without registration",
    ],
    "es": [
        "cómo {kw}", "cómo usar {kw}", "cómo acceder a {kw}",
        "cómo registrarse en {kw}", "cómo funciona {kw}",
        "dónde encontrar {kw}", "dónde jugar {kw}",
        "por qué {kw}", "por qué elegir {kw}", "por qué usar {kw}",
        "qué {kw} elegir", "cuál es el mejor {kw}",
        "es {kw} seguro", "es {kw} legal", "es {kw} confiable",
        "guía completa {kw}", "guía {kw} principiantes", "tutorial {kw}",
        "los mejores {kw}", "top 10 {kw}", "ranking {kw}",
        "opinión sobre {kw}", "reseña {kw} 2024", "vale la pena {kw}",
        "todo sobre {kw}", "{kw} para principiantes", "{kw} explicado",
        "bono {kw} sin depósito", "código promocional {kw}",
    ],
    "pt": [
        "como {kw}", "como usar {kw}", "como acessar {kw}",
        "como se cadastrar no {kw}", "como funciona {kw}",
        "onde encontrar {kw}", "onde jogar {kw}",
        "por que {kw}", "por que escolher {kw}", "por que usar {kw}",
        "qual {kw} escolher", "qual é o melhor {kw}",
        "é {kw} seguro", "é {kw} legal", "é {kw} confiável",
        "guia completo {kw}", "guia {kw} iniciantes", "tutorial {kw}",
        "os melhores {kw}", "top 10 {kw}", "ranking {kw}",
        "avaliação de {kw}", "review {kw} 2024", "vale a pena {kw}",
        "tudo sobre {kw}", "{kw} para iniciantes", "{kw} explicado",
        "bônus {kw} sem depósito", "código promocional {kw}",
    ],
    "de": [
        "wie {kw}", "wie man {kw} benutzt", "wie man auf {kw} zugreift",
        "wie man sich bei {kw} anmeldet", "wie funktioniert {kw}",
        "wo {kw} finden", "wo {kw} spielen",
        "warum {kw}", "warum {kw} wählen", "warum {kw} nutzen",
        "welche {kw} wählen", "was ist das beste {kw}",
        "ist {kw} sicher", "ist {kw} legal", "ist {kw} seriös",
        "kompletter {kw} guide", "{kw} anfänger guide", "{kw} tutorial",
        "die besten {kw}", "top 10 {kw}", "{kw} ranking",
        "{kw} bewertung", "{kw} erfahrung 2024", "lohnt sich {kw}",
        "alles über {kw}", "{kw} für anfänger", "{kw} erklärt",
        "{kw} bonus ohne einzahlung", "{kw} promo code",
    ],
    "it": [
        "come {kw}", "come usare {kw}", "come accedere a {kw}",
        "come registrarsi su {kw}", "come funziona {kw}",
        "dove trovare {kw}", "dove giocare {kw}",
        "perché {kw}", "perché scegliere {kw}", "perché usare {kw}",
        "quale {kw} scegliere", "qual è il migliore {kw}",
        "è {kw} sicuro", "è {kw} legale", "è {kw} affidabile",
        "guida completa {kw}", "guida {kw} principianti", "tutorial {kw}",
        "i migliori {kw}", "top 10 {kw}", "classifica {kw}",
        "recensione {kw}", "esperienza {kw} 2024", "vale la pena {kw}",
        "tutto su {kw}", "{kw} per principianti", "{kw} spiegato",
        "bonus {kw} senza deposito", "codice promozionale {kw}",
    ],
}


# =============================================================================
# CLASSES
# =============================================================================

@dataclass
class AnchorInput:
    url: str
    mot_cle_principal: str
    mots_cles_secondaires: list
    nom_marque: str
    nombre_liens: int
    langue: str = "fr"


class AnchorProfileGenerator:
    
    def __init__(self, inputs: AnchorInput):
        self.inputs = inputs
        self.parsed_url = urlparse(inputs.url)
        self.domain = self.parsed_url.netloc.replace("www.", "")
        self.anchors = []
    
    def _get_count(self, anchor_type: str) -> int:
        percentage = DISTRIBUTION.get(anchor_type, 0)
        count = round(self.inputs.nombre_liens * percentage / 100)
        return max(1, count) if percentage > 0 else 0
    
    def _generate_marque(self) -> list:
        count = self._get_count("marque")
        brand = self.inputs.nom_marque.strip()
        
        options = [
            brand,
            brand.lower(),
            brand.upper(),
            brand.capitalize(),
            self.domain,
            f"www.{self.domain}" if "www." in self.parsed_url.netloc else self.domain,
        ]
        
        if self.inputs.langue == "fr":
            options.extend([f"site {brand}", f"{brand} officiel", f"plateforme {brand}"])
        else:
            options.extend([f"{brand} site", f"{brand} official", f"{brand} platform"])
        
        options = list(dict.fromkeys(options))
        
        result = []
        while len(result) < count:
            result.append(random.choice(options))
        
        return result[:count]
    
    def _generate_url_nue(self) -> list:
        count = self._get_count("url_nue")
        
        has_www = "www." in self.parsed_url.netloc
        domain_as_given = self.parsed_url.netloc
        
        options = [
            self.inputs.url,
            self.inputs.url.replace("https://", "").replace("http://", ""),
            domain_as_given,
            f"https://{domain_as_given}",
        ]
        
        if self.parsed_url.path and self.parsed_url.path != "/":
            options.append(f"https://{domain_as_given}/")
            options.append(f"{domain_as_given}/")
        
        options = list(dict.fromkeys(options))
        
        result = []
        while len(result) < count:
            result.append(random.choice(options))
        
        return result[:count]
    
    def _generate_generique(self) -> list:
        count = self._get_count("generique")
        lang = self.inputs.langue if self.inputs.langue in GENERIQUES else "en"
        options = GENERIQUES[lang]
        
        result = []
        while len(result) < count:
            result.extend(random.sample(options, min(len(options), count - len(result))))
        
        return result[:count]
    
    def _generate_partielle(self) -> list:
        count = self._get_count("partielle")
        lang = self.inputs.langue if self.inputs.langue in TEMPLATES_PARTIELLES else "en"
        templates = TEMPLATES_PARTIELLES[lang]
        
        all_keywords = [self.inputs.mot_cle_principal] + self.inputs.mots_cles_secondaires
        
        options = []
        for kw in all_keywords:
            for template in templates:
                anchor = template.format(kw=kw)
                words = anchor.lower().split()
                if len(words) == len(set(words)):
                    options.append(anchor)
        
        options = list(dict.fromkeys(options))
        random.shuffle(options)
        return options[:count]
    
    def _generate_exacte(self) -> list:
        count = self._get_count("exacte")
        
        options = [self.inputs.mot_cle_principal] * 3
        options.extend(self.inputs.mots_cles_secondaires[:2])
        
        result = []
        while len(result) < count:
            result.append(random.choice(options))
        
        return result[:count]
    
    def _generate_longue_traine(self) -> list:
        count = self._get_count("longue_traine")
        lang = self.inputs.langue if self.inputs.langue in TEMPLATES_LONGUE_TRAINE else "en"
        templates = TEMPLATES_LONGUE_TRAINE[lang]
        
        all_keywords = [self.inputs.mot_cle_principal] + self.inputs.mots_cles_secondaires
        
        options = []
        for kw in all_keywords:
            for template in templates:
                anchor = template.format(kw=kw)
                words = anchor.lower().split()
                if len(words) == len(set(words)):
                    options.append(anchor)
        
        options = list(dict.fromkeys(options))
        random.shuffle(options)
        return options[:count]
    
    def generate(self) -> list:
        self.anchors = []
        
        types_generators = [
            ("marque", self._generate_marque),
            ("url_nue", self._generate_url_nue),
            ("generique", self._generate_generique),
            ("partielle", self._generate_partielle),
            ("exacte", self._generate_exacte),
            ("longue_traine", self._generate_longue_traine),
        ]
        
        for anchor_type, generator in types_generators:
            anchors = generator()
            for anchor in anchors:
                self.anchors.append({
                    "type": anchor_type,
                    "ancre": anchor,
                    "pourcentage_cible": f"{DISTRIBUTION[anchor_type]}%"
                })
        
        random.shuffle(self.anchors)
        
        return self.anchors
    
    def get_stats(self) -> dict:
        counts = {}
        for anchor in self.anchors:
            t = anchor["type"]
            counts[t] = counts.get(t, 0) + 1
        
        stats = {}
        for anchor_type, target_pct in DISTRIBUTION.items():
            actual_count = counts.get(anchor_type, 0)
            actual_pct = round(actual_count / len(self.anchors) * 100) if self.anchors else 0
            stats[anchor_type] = {
                "count": actual_count,
                "actual_pct": actual_pct,
                "target_pct": target_pct
            }
        
        return stats
    
    def to_csv(self) -> str:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["type", "ancre", "pourcentage_cible"])
        writer.writeheader()
        writer.writerows(self.anchors)
        return output.getvalue()
    
    def to_json(self) -> str:
        data = {
            "url": self.inputs.url,
            "marque": self.inputs.nom_marque,
            "mot_cle_principal": self.inputs.mot_cle_principal,
            "mots_cles_secondaires": self.inputs.mots_cles_secondaires,
            "langue": self.inputs.langue,
            "distribution_cible": DISTRIBUTION,
            "ancres": self.anchors
        }
        return json.dumps(data, ensure_ascii=False, indent=2)


# =============================================================================
# INTERFACE STREAMLIT
# =============================================================================

def main():
    st.set_page_config(
        page_title="Générateur d'Ancres",
        page_icon="🔗",
        layout="wide"
    )
    
    st.title("🔗 Générateur de Profil d'Ancres")
    st.markdown("Génère un profil d'ancres naturel pour vos campagnes de link building.")
    
    # Sidebar pour les inputs
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        url = st.text_input("🎯 URL cible", placeholder="https://example.com/page/")
        nom_marque = st.text_input("🏷️ Nom de marque", placeholder="Ma Marque")
        mot_cle_principal = st.text_input("🔑 Mot-clé principal", placeholder="casino en ligne")
        mots_cles_secondaires = st.text_area(
            "🔑 Mots-clés secondaires (un par ligne)",
            placeholder="bonus casino\navis casino\ncode promo",
            height=120
        )
        
        col1, col2 = st.columns(2)
        with col1:
            nombre_liens = st.number_input("📊 Nombre de liens", min_value=5, max_value=500, value=30)
        with col2:
            langue = st.selectbox("🌐 Langue", ["fr", "en", "es", "pt", "de", "it"], index=0)
        
        generate_button = st.button("🚀 Générer le profil", type="primary", use_container_width=True)
    
    # Zone principale
    if generate_button:
        if not url or not nom_marque or not mot_cle_principal:
            st.error("⚠️ Veuillez remplir l'URL, le nom de marque et le mot-clé principal.")
        else:
            # Parser les mots-clés secondaires
            mcs_list = [kw.strip() for kw in mots_cles_secondaires.split("\n") if kw.strip()]
            
            # Créer les inputs
            inputs = AnchorInput(
                url=url.strip(),
                mot_cle_principal=mot_cle_principal.strip(),
                mots_cles_secondaires=mcs_list,
                nom_marque=nom_marque.strip(),
                nombre_liens=nombre_liens,
                langue=langue
            )
            
            # Générer
            generator = AnchorProfileGenerator(inputs)
            generator.generate()
            stats = generator.get_stats()
            
            # Afficher les stats
            st.subheader("📊 Distribution")
            
            cols = st.columns(6)
            for i, (anchor_type, data) in enumerate(stats.items()):
                with cols[i]:
                    st.metric(
                        label=anchor_type.replace("_", " ").upper(),
                        value=f"{data['count']}",
                        delta=f"{data['actual_pct']}% / {data['target_pct']}%"
                    )
            
            # Afficher le tableau
            st.subheader(f"📝 Liste des ancres ({len(generator.anchors)} générées)")
            
            # Convertir en format pour affichage
            import pandas as pd
            df = pd.DataFrame(generator.anchors)
            df.index = df.index + 1
            df.columns = ["Type", "Ancre", "% Cible"]
            
            st.dataframe(df, use_container_width=True, height=400)
            
            # Boutons d'export
            st.subheader("💾 Exporter")
            
            col1, col2 = st.columns(2)
            
            with col1:
                csv_data = generator.to_csv()
                st.download_button(
                    label="📥 Télécharger CSV",
                    data=csv_data,
                    file_name=f"ancres_{nom_marque.lower().replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                json_data = generator.to_json()
                st.download_button(
                    label="📥 Télécharger JSON",
                    data=json_data,
                    file_name=f"ancres_{nom_marque.lower().replace(' ', '_')}.json",
                    mime="application/json",
                    use_container_width=True
                )
    
    else:
        # Message d'accueil
        st.info("👈 Remplissez les champs dans la barre latérale et cliquez sur **Générer le profil**")
        
        # Afficher la distribution cible
        st.subheader("📈 Distribution cible par défaut")
        
        cols = st.columns(6)
        for i, (anchor_type, pct) in enumerate(DISTRIBUTION.items()):
            with cols[i]:
                st.metric(label=anchor_type.replace("_", " ").upper(), value=f"{pct}%")


if __name__ == "__main__":
    main()
