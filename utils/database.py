import mysql.connector
from utils.logger import logger
from utils.config import Config


class Database:
    @staticmethod
    def get_random_payment():
        try:
            logger.info("Connexion à la base de données")
            conn = mysql.connector.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME
            )
            cursor = conn.cursor()
            cursor.execute("SELECT email, numero_visa, mm_aa, cvv, zip_code FROM paiement ORDER BY RAND() LIMIT 1")
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if not result:
                raise Exception("Aucune donnée de paiement trouvée")

            logger.info("Données de paiement récupérées avec succès")
            return result
        except mysql.connector.Error as err:
            logger.error(f"Erreur base de données: {err}")
            raise