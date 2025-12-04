# 🔗 Générateur de Profil d'Ancres

Application web pour générer des profils d'ancres naturels pour vos campagnes de link building.

## 🚀 Déploiement rapide (Streamlit Cloud - GRATUIT)

### Option 1 : Streamlit Cloud (Recommandé)

1. **Créer un repo GitHub** avec ces fichiers :
   - `app.py`
   - `requirements.txt`

2. **Aller sur** [share.streamlit.io](https://share.streamlit.io)

3. **Se connecter** avec GitHub

4. **Cliquer** "New app" → Sélectionner ton repo → Deploy

5. **URL générée** : `https://ton-app.streamlit.app`

**Temps de déploiement : ~2 minutes**

---

### Option 2 : Serveur VPS (Ubuntu)

```bash
# Installer les dépendances
sudo apt update
sudo apt install python3-pip python3-venv -y

# Créer l'environnement
mkdir anchor-generator && cd anchor-generator
python3 -m venv venv
source venv/bin/activate

# Installer les packages
pip install streamlit pandas

# Copier app.py ici

# Lancer (dev)
streamlit run app.py --server.port 8501

# Lancer (prod avec screen)
screen -S anchor
streamlit run app.py --server.port 8501 --server.headless true
# Ctrl+A, D pour détacher
```

**Accès** : `http://IP_DU_SERVEUR:8501`

---

### Option 3 : Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"]
```

```bash
docker build -t anchor-generator .
docker run -d -p 8501:8501 anchor-generator
```

---

### Option 4 : Railway / Render / Heroku

Ces plateformes détectent automatiquement Streamlit. Il suffit de :
1. Connecter ton repo GitHub
2. Déployer

Pour **Heroku**, ajouter un fichier `Procfile` :
```
web: streamlit run app.py --server.port $PORT --server.headless true
```

---

## 📊 Distribution des ancres

| Type | Pourcentage |
|------|-------------|
| Marque | 35% |
| URL nue | 20% |
| Générique | 20% |
| Partielle | 15% |
| Exacte | 5% |
| Longue traîne | 5% |

---

## 🌐 Langues supportées

- 🇫🇷 Français (fr)
- 🇬🇧 English (en)
- 🇪🇸 Español (es)
- 🇵🇹 Português (pt)
- 🇩🇪 Deutsch (de)
- 🇮🇹 Italiano (it)

---

## 📝 Utilisation

1. Remplir l'URL cible
2. Entrer le nom de marque
3. Ajouter le mot-clé principal
4. Ajouter les mots-clés secondaires (un par ligne)
5. Choisir le nombre de liens et la langue
6. Cliquer "Générer le profil"
7. Exporter en CSV ou JSON
