import configparser
import os


class Config:
    # Chemin absolu du fichier config.ini
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(BASE_DIR, '..', 'config.ini')

    # Lire la configuration
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    # Paramètres de la base de données
    DB_HOST = config.get('DATABASE', 'host')
    DB_USER = config.get('DATABASE', 'user')
    DB_PASSWORD = config.get('DATABASE', 'password')
    DB_NAME = config.get('DATABASE', 'database')

    # Paramètres web
    BASE_URL = config.get('WEB', 'base_url')

    # Paramètres navigateur
    browser_headless = config.getboolean('BROWSER', 'headless', fallback=False)

    # Paramètres d'attente
    WAIT_TIMEOUT = config.getint('WAIT', 'timeout', fallback=30)