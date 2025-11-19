# Guide d'utilisation de scraper_utils.py

## Description

`scraper_utils.py` contient des fonctions utilitaires pour scraper des tableaux HTML depuis des sites web utilisant du JavaScript dynamique.

## Fonctions disponibles

### 1. `scrape_table_from_url()`

Scrape un tableau HTML depuis une URL et le convertit en DataFrame pandas.

**Paramètres:**
- `url` (str): L'URL de la page contenant le tableau
- `headless` (bool, optionnel): Exécuter Chrome sans interface graphique (défaut: True)
- `timeout_secs` (int, optionnel): Temps d'attente maximum pour le chargement du tableau (défaut: 30)
- `chrome_options` (Options, optionnel): Options Chrome personnalisées

**Retourne:**
- `pd.DataFrame`: Le tableau extrait sous forme de DataFrame

### 2. `close_browser()`

Ferme toutes les instances de navigateur ouvertes pour libérer les ressources.

## Comment importer dans un autre notebook

### Méthode 1: Import simple (notebooks dans le même dossier)

```python
# Dans votre notebook Jupyter
from scraper_utils import scrape_table_from_url, close_browser

# Utilisation
url = 'https://ourworldindata.org/grapher/electricity-generation?tab=table'
df = scrape_table_from_url(url)
close_browser()
```

### Méthode 2: Import avec gestion du path (si les fichiers sont dans des dossiers différents)

```python
import sys
import os

# Ajouter le chemin du dossier contenant scraper_utils.py
sys.path.append(os.path.abspath('../chemin/vers/le/dossier'))

from scraper_utils import scrape_table_from_url, close_browser
```

### Méthode 3: Import relatif (si vous avez une structure de package)

```python
# Si votre structure est:
# projet/
#   ├── utils/
#   │   └── scraper_utils.py
#   └── notebooks/
#       └── analyse.ipynb

import sys
sys.path.append('..')

from utils.scraper_utils import scrape_table_from_url
```

## Exemples d'utilisation

### Exemple 1: Utilisation basique

```python
from scraper_utils import scrape_table_from_url, close_browser
import pandas as pd

# Scraper un tableau
url = 'https://ourworldindata.org/grapher/electricity-generation?tab=table'
df = scrape_table_from_url(url)

# Afficher le résultat
print(df.head())
print(f"Shape: {df.shape}")

# Fermer le navigateur
close_browser()
```

### Exemple 2: Avec options Chrome personnalisées

```python
from scraper_utils import scrape_table_from_url, close_browser
from selenium.webdriver.chrome.options import Options

# Créer des options personnalisées
opts = Options()
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument('--window-size=1920,1080')

# Scraper avec les options
df = scrape_table_from_url(
    url='https://example.com/data',
    headless=True,
    timeout_secs=45,
    chrome_options=opts
)

close_browser()
```

### Exemple 3: Mode non-headless (pour déboguer)

```python
from scraper_utils import scrape_table_from_url, close_browser

# Voir le navigateur s'exécuter (utile pour le débogage)
df = scrape_table_from_url(
    url='https://example.com/data',
    headless=False  # Le navigateur sera visible
)

close_browser()
```

## Dépendances requises

Assurez-vous d'avoir installé les packages suivants:

```bash
pip install helium selenium beautifulsoup4 pandas
```

## Structure du projet

```
Dataviz_Africitizen_project/
├── scraper_utils.py          # Module avec les fonctions
├── energy.ipynb               # Notebook principal (utilise scraper_utils)
|
├── Exploratory_analysis.ipynb # Autre notebook (scraper_utils specialement destiné à nettoyer les données scrapées du notebook  principal et faire de l'analyse  )
└── SCRAPER_USAGE.md          # Ce fichier
```

## Conseils et bonnes pratiques

1. **Toujours fermer le navigateur**: Utilisez `close_browser()` à la fin pour libérer les ressources

2. **Gestion des erreurs**: La fonction retourne un DataFrame vide si aucune table n'est trouvée

3. **Timeout**: Augmentez `timeout_secs` si le site met du temps à charger

4. **Mode headless**: Utilisez `headless=False` pour déboguer visuellement le scraping

5. **Réutilisation**: Vous pouvez appeler la fonction plusieurs fois pour différentes URLs

## Dépannage

### Problème: "ModuleNotFoundError: No module named 'scraper_utils'"

**Solution**: Assurez-vous que:
- Le fichier `scraper_utils.py` est dans le même dossier que votre notebook
- Ou ajoutez le chemin avec `sys.path.append()`

### Problème: "Table not found within timeout"

**Solutions**:
- Augmentez le `timeout_secs`
- Vérifiez que la page contient bien un élément `<table>`
- Utilisez `headless=False` pour voir ce que le navigateur affiche

### Problème: Le DataFrame est vide

**Solutions**:
- Le site utilise peut-être un iframe ou un format de table différent
- Vérifiez manuellement la structure HTML de la page
- Essayez d'augmenter le temps d'attente

## Support

Pour toute question ou problème, consultez la documentation de:
- [Helium](https://github.com/mherrmann/selenium-python-helium)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Pandas](https://pandas.pydata.org/docs/)
