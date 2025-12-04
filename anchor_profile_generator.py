#!/usr/bin/env python3
"""
Générateur de profil d'ancres pour link building
Génère une liste d'ancres naturelles basée sur les inputs utilisateur
"""

import random
import csv
import json
from urllib.parse import urlparse
from dataclasses import dataclass
from typing import Optional


# =============================================================================
# CONFIGURATION DES DISTRIBUTIONS ET TEMPLATES
# =============================================================================

DISTRIBUTION = {
    "marque": 35,           # Nom de marque / domaine
    "url_nue": 20,          # URL brute
    "generique": 20,        # Cliquez ici, en savoir plus...
    "partielle": 15,        # Mot-clé + variation
    "exacte": 5,            # Mot-clé exact
    "longue_traine": 5,     # Questions / expressions longues
}

GENERIQUES = {
    "fr": [
        "cliquez ici", "en savoir plus", "voir le site", "lire la suite",
        "plus d'infos", "découvrir", "visiter", "sur ce site", "ici",
        "ce lien", "cette page", "voir ici", "consultez", "accéder",
        "plus de détails", "lire l'article", "voir l'article"
    ],
    "en": [
        "click here", "learn more", "read more", "visit website",
        "more info", "discover", "check this out", "this site", "here",
        "this link", "this page", "see here", "find out more", "view more"
    ],
    "es": [
        "haz clic aquí", "saber más", "leer más", "visitar sitio",
        "más información", "descubrir", "ver aquí", "este sitio",
        "aquí", "este enlace", "esta página", "ver más", "acceder"
    ],
    "pt": [
        "clique aqui", "saiba mais", "leia mais", "visitar site",
        "mais informações", "descobrir", "ver aqui", "este site",
        "aqui", "este link", "esta página", "ver mais", "acessar"
    ],
    "de": [
        "hier klicken", "mehr erfahren", "weiterlesen", "Webseite besuchen",
        "mehr Infos", "entdecken", "hier ansehen", "diese Seite",
        "hier", "dieser Link", "diese Seite", "mehr sehen", "zugreifen"
    ],
    "it": [
        "clicca qui", "scopri di più", "leggi di più", "visita il sito",
        "maggiori informazioni", "scoprire", "vedi qui", "questo sito",
        "qui", "questo link", "questa pagina", "vedi altro", "accedi"
    ],
}

TEMPLATES_PARTIELLES = {
    "fr": [
        "{kw} en ligne", "{kw} 2024", "{kw} 2025", "guide {kw}", "meilleur {kw}",
        "{kw} avis", "{kw} comparatif", "tout sur {kw}", "{kw} france",
        "{kw} gratuit", "top {kw}", "{kw} fiable", "{kw} sécurisé"
    ],
    "en": [
        "{kw} online", "{kw} 2024", "{kw} 2025", "{kw} guide", "best {kw}",
        "{kw} review", "{kw} comparison", "all about {kw}", "{kw} uk",
        "free {kw}", "top {kw}", "trusted {kw}", "safe {kw}"
    ],
    "es": [
        "{kw} online", "{kw} 2024", "{kw} 2025", "guía {kw}", "mejor {kw}",
        "{kw} opiniones", "{kw} comparativa", "todo sobre {kw}",
        "{kw} gratis", "top {kw}", "{kw} seguro", "{kw} fiable"
    ],
    "pt": [
        "{kw} online", "{kw} 2024", "{kw} 2025", "guia {kw}", "melhor {kw}",
        "{kw} avaliação", "{kw} comparação", "tudo sobre {kw}",
        "{kw} grátis", "top {kw}", "{kw} seguro", "{kw} confiável"
    ],
    "de": [
        "{kw} online", "{kw} 2024", "{kw} 2025", "{kw} Guide", "beste {kw}",
        "{kw} Bewertung", "{kw} Vergleich", "alles über {kw}",
        "{kw} kostenlos", "top {kw}", "{kw} sicher", "{kw} seriös"
    ],
    "it": [
        "{kw} online", "{kw} 2024", "{kw} 2025", "guida {kw}", "migliore {kw}",
        "{kw} recensione", "{kw} confronto", "tutto su {kw}",
        "{kw} gratis", "top {kw}", "{kw} sicuro", "{kw} affidabile"
    ],
}

TEMPLATES_LONGUE_TRAINE = {
    "fr": [
        "comment {kw}", "où trouver {kw}", "pourquoi {kw}",
        "quel {kw} choisir", "guide complet {kw}", "tout savoir sur {kw}",
        "les meilleurs {kw}", "avis sur {kw}", "{kw} pour débutants"
    ],
    "en": [
        "how to {kw}", "where to find {kw}", "why {kw}",
        "which {kw} to choose", "complete {kw} guide", "all about {kw}",
        "the best {kw}", "{kw} review", "{kw} for beginners"
    ],
    "es": [
        "cómo {kw}", "dónde encontrar {kw}", "por qué {kw}",
        "qué {kw} elegir", "guía completa {kw}", "todo sobre {kw}",
        "los mejores {kw}", "opinión sobre {kw}", "{kw} para principiantes"
    ],
    "pt": [
        "como {kw}", "onde encontrar {kw}", "por que {kw}",
        "qual {kw} escolher", "guia completo {kw}", "tudo sobre {kw}",
        "os melhores {kw}", "avaliação de {kw}", "{kw} para iniciantes"
    ],
    "de": [
        "wie {kw}", "wo {kw} finden", "warum {kw}",
        "welche {kw} wählen", "kompletter {kw} Guide", "alles über {kw}",
        "die besten {kw}", "{kw} Bewertung", "{kw} für Anfänger"
    ],
    "it": [
        "come {kw}", "dove trovare {kw}", "perché {kw}",
        "quale {kw} scegliere", "guida completa {kw}", "tutto su {kw}",
        "i migliori {kw}", "recensione {kw}", "{kw} per principianti"
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
        """Calcule le nombre d'ancres pour un type donné"""
        percentage = DISTRIBUTION.get(anchor_type, 0)
        count = round(self.inputs.nombre_liens * percentage / 100)
        return max(1, count) if percentage > 0 else 0
    
    def _generate_marque(self) -> list:
        """Génère les ancres de type marque"""
        count = self._get_count("marque")
        brand = self.inputs.nom_marque.strip()
        
        # Options d'ancres marque - UNIQUEMENT le nom de marque et ses variations
        options = [
            brand,                      # Betify
            brand.lower(),              # betify
            brand.upper(),              # BETIFY
            brand.capitalize(),         # Betify
            self.domain,                # betify-eu.net
            f"www.{self.domain}",       # www.betify-eu.net
        ]
        
        # Ajouter des variations contextuelles selon la langue
        if self.inputs.langue == "fr":
            options.extend([
                f"site {brand}",
                f"{brand} officiel",
                f"plateforme {brand}",
            ])
        else:
            options.extend([
                f"{brand} site",
                f"{brand} official",
                f"{brand} platform",
            ])
        
        # Supprimer les doublons
        options = list(dict.fromkeys(options))
        
        # Sélectionner aléatoirement
        result = []
        while len(result) < count:
            pick = random.choice(options)
            result.append(pick)
        
        return result[:count]
    
    def _generate_url_nue(self) -> list:
        """Génère les ancres URL nues"""
        count = self._get_count("url_nue")
        
        options = [
            self.inputs.url,
            self.inputs.url.replace("https://", "").replace("http://", ""),
            self.domain,
            f"https://{self.domain}",
            f"www.{self.domain}",
        ]
        
        result = []
        while len(result) < count:
            result.extend(random.sample(options, min(len(options), count - len(result))))
        
        return result[:count]
    
    def _generate_generique(self) -> list:
        """Génère les ancres génériques"""
        count = self._get_count("generique")
        lang = self.inputs.langue if self.inputs.langue in GENERIQUES else "en"
        options = GENERIQUES[lang]
        
        result = []
        while len(result) < count:
            result.extend(random.sample(options, min(len(options), count - len(result))))
        
        return result[:count]
    
    def _generate_partielle(self) -> list:
        """Génère les ancres partielles (mot-clé + variation)"""
        count = self._get_count("partielle")
        lang = self.inputs.langue if self.inputs.langue in TEMPLATES_PARTIELLES else "en"
        templates = TEMPLATES_PARTIELLES[lang]
        
        # Combiner mot-clé principal et secondaires
        all_keywords = [self.inputs.mot_cle_principal] + self.inputs.mots_cles_secondaires
        
        options = []
        for kw in all_keywords:
            kw_lower = kw.lower()
            for template in templates:
                anchor = template.format(kw=kw)
                # Éviter les doublons de mots (ex: "betify avis avis")
                words = anchor.lower().split()
                if len(words) == len(set(words)):  # Pas de mot en double
                    options.append(anchor)
        
        # Supprimer les doublons exacts
        options = list(dict.fromkeys(options))
        random.shuffle(options)
        return options[:count]
    
    def _generate_exacte(self) -> list:
        """Génère les ancres exactes"""
        count = self._get_count("exacte")
        
        # Principalement le mot-clé principal, avec quelques secondaires
        options = [self.inputs.mot_cle_principal] * 3
        options.extend(self.inputs.mots_cles_secondaires[:2])
        
        result = []
        while len(result) < count:
            result.append(random.choice(options))
        
        return result[:count]
    
    def _generate_longue_traine(self) -> list:
        """Génère les ancres longue traîne"""
        count = self._get_count("longue_traine")
        lang = self.inputs.langue if self.inputs.langue in TEMPLATES_LONGUE_TRAINE else "en"
        templates = TEMPLATES_LONGUE_TRAINE[lang]
        
        all_keywords = [self.inputs.mot_cle_principal] + self.inputs.mots_cles_secondaires
        
        options = []
        for kw in all_keywords:
            for template in templates:
                anchor = template.format(kw=kw)
                # Éviter les doublons de mots
                words = anchor.lower().split()
                if len(words) == len(set(words)):
                    options.append(anchor)
        
        # Supprimer les doublons exacts
        options = list(dict.fromkeys(options))
        random.shuffle(options)
        return options[:count]
    
    def generate(self) -> list:
        """Génère le profil complet d'ancres"""
        self.anchors = []
        
        # Générer chaque type
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
        
        # Mélanger pour un ordre naturel
        random.shuffle(self.anchors)
        
        return self.anchors
    
    def display(self):
        """Affiche le profil d'ancres"""
        print("\n" + "=" * 70)
        print("🔗 PROFIL D'ANCRES GÉNÉRÉ")
        print("=" * 70)
        
        print(f"\n🎯 URL cible     : {self.inputs.url}")
        print(f"🏷️  Marque        : {self.inputs.nom_marque}")
        print(f"🔑 MC principal  : {self.inputs.mot_cle_principal}")
        print(f"🔑 MC secondaires: {', '.join(self.inputs.mots_cles_secondaires)}")
        print(f"📊 Nombre liens  : {self.inputs.nombre_liens}")
        print(f"🌐 Langue        : {self.inputs.langue.upper()}")
        
        print("\n" + "-" * 70)
        print("📋 DISTRIBUTION")
        print("-" * 70)
        
        # Compter par type
        counts = {}
        for anchor in self.anchors:
            t = anchor["type"]
            counts[t] = counts.get(t, 0) + 1
        
        for anchor_type, target_pct in DISTRIBUTION.items():
            actual_count = counts.get(anchor_type, 0)
            actual_pct = round(actual_count / len(self.anchors) * 100) if self.anchors else 0
            print(f"  {anchor_type.upper():15} : {actual_count:3} ancres ({actual_pct}% réel / {target_pct}% cible)")
        
        print("\n" + "-" * 70)
        print("📝 LISTE DES ANCRES")
        print("-" * 70)
        
        for i, anchor in enumerate(self.anchors, 1):
            print(f"  {i:3}. [{anchor['type']:12}] {anchor['ancre']}")
        
        print("\n" + "=" * 70)
        print(f"✅ Total : {len(self.anchors)} ancres générées")
        print("=" * 70)
    
    def export_csv(self, filename: str = "profil_ancres.csv"):
        """Exporte en CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["type", "ancre", "pourcentage_cible"])
            writer.writeheader()
            writer.writerows(self.anchors)
        print(f"\n✅ Exporté vers {filename}")
    
    def export_json(self, filename: str = "profil_ancres.json"):
        """Exporte en JSON"""
        data = {
            "url": self.inputs.url,
            "marque": self.inputs.nom_marque,
            "mot_cle_principal": self.inputs.mot_cle_principal,
            "mots_cles_secondaires": self.inputs.mots_cles_secondaires,
            "langue": self.inputs.langue,
            "distribution_cible": DISTRIBUTION,
            "ancres": self.anchors
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Exporté vers {filename}")


# =============================================================================
# INTERFACE CLI
# =============================================================================

def main():
    print("\n" + "=" * 50)
    print("🔗 GÉNÉRATEUR DE PROFIL D'ANCRES")
    print("=" * 50)
    
    # Collecte des inputs
    url = input("\n📎 URL cible: ").strip()
    mot_cle_principal = input("🔑 Mot-clé principal: ").strip()
    mots_cles_secondaires = input("🔑 Mots-clés secondaires (virgules): ").strip()
    mots_cles_secondaires = [kw.strip() for kw in mots_cles_secondaires.split(",") if kw.strip()]
    
    nom_marque = input("🏷️  Nom de marque: ").strip()
    
    try:
        nombre_liens = int(input("📊 Nombre de liens prévus: ").strip())
    except ValueError:
        nombre_liens = 20
    
    langue = input("🌐 Langue (fr/en/es/pt/de/it): ").strip().lower() or "fr"
    
    # Création des inputs
    inputs = AnchorInput(
        url=url,
        mot_cle_principal=mot_cle_principal,
        mots_cles_secondaires=mots_cles_secondaires,
        nom_marque=nom_marque,
        nombre_liens=nombre_liens,
        langue=langue
    )
    
    # Génération
    generator = AnchorProfileGenerator(inputs)
    generator.generate()
    generator.display()
    
    # Export
    export = input("\n💾 Exporter? (csv/json/non): ").strip().lower()
    if export == "csv":
        generator.export_csv()
    elif export == "json":
        generator.export_json()
    
    print("\n✨ Terminé!\n")


if __name__ == "__main__":
    main()
