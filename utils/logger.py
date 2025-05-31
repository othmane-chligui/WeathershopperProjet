import logging
import os
from utils.config import Config

# Créer le dossier logs si nécessaire
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'test.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("WeathershopperTest")