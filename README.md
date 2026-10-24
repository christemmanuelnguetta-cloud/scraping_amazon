# Amazon Scraper — casques Bluetooth sans fil

Petit scraper Amazon piloté uniquement avec Selenium. Il récupère au maximum 10 casques Bluetooth sans fil depuis une page de résultats, affiche les produits dans le terminal et enregistre les résultats dans une base SQLite.

## Prérequis

- Python 3.10 ou plus récent
- Google Chrome installé
- Connexion Internet

Selenium Manager essaie de gérer automatiquement le pilote du navigateur. Aucune bibliothèque HTTP, aucun parseur HTML externe et aucun navigateur automatisé autre que Selenium ne sont utilisés.

## Installation

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Lancement automatique

Depuis le terminal VS Code ouvert dans le dossier du projet :

```powershell
python main.py
```

Par défaut, Chrome s'ouvre à l'écran et Selenium le pilote automatiquement : aucune interaction manuelle n'est requise. À la fin, Chrome se ferme et les résultats sont enregistrés dans `data/casques_bluetooth.db`. Pour exécuter la collecte sans fenêtre, ajoute `--headless`.

Pour exécuter le scraping sans ouvrir de fenêtre :

```powershell
python main.py --headless
```

Options supplémentaires :

```powershell
python main.py --url https://www.amazon.fr/s?k=casque+bluetooth+sans+fil --limit 10
```

`--limit` est borné entre 1 et 10. Pour choisir l'emplacement de la base, utiliser `--database chemin/vers/fichier.db`.

## Données enregistrées

Les résultats se trouvent dans la table `produits` de `data/casques_bluetooth.db`. Chaque ligne peut contenir le titre, le prix, la note, le nombre d'avis, la référence (URL de la fiche produit) et l'image (URL). Une nouvelle collecte met à jour un produit déjà enregistré lorsque sa référence existe.

Amazon peut afficher une page d'erreur, un CAPTCHA ou modifier son interface ; dans ces cas, la collecte ne peut pas terminer normalement. Le scraper ne contourne pas les CAPTCHA ni les contrôles d'accès.

