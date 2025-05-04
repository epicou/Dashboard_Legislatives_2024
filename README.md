
# Dashboard Législatives 2024 - Paris

Ce tableau de bord interactif permet de visualiser :
- Les résultats électoraux par quartier (partis principaux).
- Les indicateurs sociaux (pauvreté, chômage, pensions, prestations).
- Des filtres interactifs : partis, indicateur social, quartiers.

## Fichiers

- `app_legislatives_2024_avance.py` : Code principal de l'application Streamlit.
- `requirements.txt` : Bibliothèques nécessaires.
- `README.md` : Ce fichier d'explication.

## Installation locale

1. Installer Python 3 : [Télécharger Python](https://www.python.org/downloads/)
2. Installer les dépendances :
```bash
pip install -r requirements.txt
```
3. Placer votre fichier Excel `Législatives 2024 Geo v1.0.xlsx` dans le même dossier.
4. Lancer l'application :
```bash
streamlit run app_legislatives_2024_avance.py
```

## Déploiement sur Streamlit Cloud

1. Créer un compte sur [Streamlit Cloud](https://streamlit.io/cloud) et sur [GitHub](https://github.com/).
2. Créer un nouveau dépôt GitHub et y ajouter :
    - `app_legislatives_2024_avance.py`
    - `requirements.txt`
    - `Législatives 2024 Geo v1.0.xlsx`
3. Depuis Streamlit Cloud :
    - Cliquez sur **New app**.
    - Connectez le dépôt GitHub.
    - Sélectionnez `app_legislatives_2024_avance.py`.
    - Cliquez sur **Deploy**.

## Fonctionnalités

- Sélecteur de partis.
- Sélecteur d'indicateur social.
- Sélecteur de quartiers.
- Carte interactive Plotly avec couleurs des partis.
- Résultats détaillés affichés sous la carte.
