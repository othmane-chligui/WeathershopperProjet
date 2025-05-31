# WeatherShopper Automation Test Project


Ce projet automatisé teste le site WeatherShopper qui adapte ses produits en fonction de la température actuelle. Le script sélectionne les produits les moins chers selon les conditions météorologiques, complète le processus d'achat et vérifie le paiement.

## Fonctionnalités principales
- Lecture automatique de la température
- Sélection intelligente des produits (moisturizers ou sunscreens)
- Ajout au panier des produits les moins chers
- Processus de paiement automatisé avec données aléatoires
- Validation des résultats de paiement
- Génération de rapports Allure avec captures d'écran
- Journalisation complète des tests
- Structure modulaire (Page Object Model)

## Prérequis
- Python 3.10+
- MySQL Server
- Microsoft Edge WebDriver (compatible avec votre version de Edge)
- Allure Commandline (pour la génération des rapports)

## Structure du projet
```
weathershopper-automation/
├── config.ini               # Fichier de configuration
├── conftest.py              # Configuration Pytest et Allure
├── requirements.txt         # Dépendances Python
├── README.md                # Ce fichier
├── pages/                   # Modèle Page Object
│   ├── base_page.py
│   ├── home_page.py
│   ├── products_page.py
│   ├── cart_page.py
│   └── payment_page.py
├── tests/                   # Tests automatisés
│   └── test_weathershopper.py
└── utils/                   # Utilitaires
    ├── config.py
    ├── database.py
    └── logger.py
```

## Installation

1. Cloner le dépôt :
   ```cmd
   git clone https://github.com/othmane-chligui/WeathershopperProjet
   cd weathershopper-automation
   ```
2. Installer les dépendances :
   ```cmd
   pip install -r requirements.txt
   ```
3. Installer Allure Commandline :
   - Télécharger Allure : https://github.com/allure-framework/allure2/releases
   - Extraire et ajouter le dossier `bin` au PATH

4. Configurer la base de données :
   - Créer une base MySQL nommée `paybase`
   - Créer la table `paiement` :
     ```sql
     CREATE TABLE paiement (
         id INT AUTO_INCREMENT PRIMARY KEY,
         email VARCHAR(255) NOT NULL,
         numero_visa VARCHAR(16) NOT NULL,
         mm_aa VARCHAR(5) NOT NULL,
         cvv VARCHAR(3) NOT NULL,
         zip_code VARCHAR(10) NOT NULL
     );
     ```
   - Insérer des données de test (exemple) :
     ```sql
     INSERT INTO paiement (email, numero_visa, mm_aa, cvv, zip_code) VALUES
     ('test1@example.com', '4242424242424242', '12/25', '123', '75001'),
     ('test2@example.com', '5555555555554444', '06/24', '456', '13001'),
     ('test3@example.com', '378282246310005', '03/26', '789', '69002');
     ```

## Configuration

Éditer le fichier `config.ini` selon votre environnement :
```ini
[DATABASE]
host = localhost
user = root
password = 
database = paybase

[WEB]
base_url = https://weathershopper.pythonanywhere.com

[BROWSER]
headless = False  # True pour exécution sans interface

[WAIT]
timeout = 30  # Délai d'attente maximum en secondes

[LOGGING]
level = INFO  # DEBUG, INFO, WARNING, ERROR

[REPORT]
allure_dir = allure-results
screenshot_on_pass = False  # True pour capturer même sur succès
```

## Exécution des tests

```cmd
Exécuter tous les tests
pytest

Exécuter avec journalisation détaillée
pytest -v

Exécuter en mode headless (sans interface)
Modifier config.ini : headless = True
```

## Génération des rapports

```cmd
Collecter les résultats des tests
pytest --alluredir=allure-results

Générer le rapport HTML
allure generate allure-results -o allure-report --clean

Ouvrir le rapport dans le navigateur
allure open allure-report
```

## Flux de test
1. Accès à la page d'accueil
2. Lecture de la température
3. Décision d'achat :
   - <19°C : Achat de moisturizers
   - >34°C : Achat de sunscreens
   - 19-34°C : Test ignoré
4. Sélection des produits :
   - Moisturizers : Aloe le moins cher + Almond le moins cher
   - Sunscreens : SPF-50 le moins cher + SPF-30 le moins cher
5. Vérification du panier (2 articles)
6. Processus de paiement avec données aléatoires
7. Validation du résultat du paiement

## Personnalisation
- Modifier les délais d'attente : `config.ini` > `[WAIT] timeout`
- Changer de navigateur : Modifier `conftest.py` (remplacer EdgeDriver par ChromeDriver ou autre)
- Ajouter des données de test : Insérer de nouvelles lignes dans la table `paiement`
- Captures d'écran supplémentaires : Ajouter dans les méthodes de page ou les tests

## Dépannage courant

**NameError: name 'EC' is not defined**
- Solution : Vérifier que tous les fichiers dans `pages/` importent :
  ```python
  from selenium.webdriver.support import expected_conditions as EC
  ```

**Échec de connexion à MySQL**
- Solution :
  - Vérifier que MySQL est démarré
  - Vérifier les identifiants dans `config.ini`
  - Tester la connexion avec :
    ```cmd
    mysql -u root -p -e "USE paybase; SELECT * FROM paiement LIMIT 1;"
    ```

**Allure ne génère pas de rapport**
- Solution :
  - Vérifier que allure-commandline est dans le PATH
  - Vérifier les permissions sur le dossier `allure-results`

**Éléments non trouvés**
- Solution :
  - Augmenter le timeout dans `config.ini`
  - Vérifier que le site est accessible
  - Mettre à jour le WebDriver
