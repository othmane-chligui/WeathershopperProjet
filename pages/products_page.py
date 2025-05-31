from .base_page import BasePage
from selenium.webdriver.common.by import By
import re
from utils.logger import logger
import time


class ProductsPage(BasePage):
    PRODUCT_CONTAINER = (By.CSS_SELECTOR, "div.text-center.col-4")
    PRODUCT_NAME = (By.CSS_SELECTOR, "p.font-weight-bold")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "p:nth-child(3)")
    ADD_BUTTON = (By.TAG_NAME, "button")
    CART_BUTTON = (By.ID, "cart")

    def get_products(self):
        return self.driver.find_elements(*self.PRODUCT_CONTAINER)

    def add_moisturizers(self):
        products = self.get_products()
        aloe_products = []
        almond_products = []

        logger.info(f"{len(products)} produits trouvés")
        assert len(products) > 0, "Aucun produit trouvé"

        for product in products:
            try:
                name = product.find_element(*self.PRODUCT_NAME).text
                price_text = product.find_element(*self.PRODUCT_PRICE).text
                price = int(re.search(r'\d+', price_text).group())
                button = product.find_element(*self.ADD_BUTTON)

                if "aloe" in name.lower():
                    aloe_products.append((price, name, button))
                elif "almond" in name.lower():
                    almond_products.append((price, name, button))

            except Exception as e:
                logger.warning(f"Erreur traitement produit: {str(e)}")
                continue

        # Sélection des produits
        time.sleep(0.5)
        self._select_product(aloe_products, "Aloe")
        time.sleep(0.5)
        self._select_product(almond_products, "Almond")

        # Accès au panier
        time.sleep(0.5)
        self.click(self.CART_BUTTON, "Bouton panier")

    def add_sunscreens(self):
        products = self.get_products()
        spf50_products = []
        spf30_products = []

        logger.info(f"{len(products)} produits trouvés")
        assert len(products) > 0, "Aucun produit trouvé"

        for product in products:
            try:
                name = product.find_element(*self.PRODUCT_NAME).text
                price_text = product.find_element(*self.PRODUCT_PRICE).text
                price = int(re.search(r'\d+', price_text).group())
                button = product.find_element(*self.ADD_BUTTON)
                spf = self._extract_spf(name)

                if spf == "50":
                    spf50_products.append((price, name, button))
                elif spf == "30":
                    spf30_products.append((price, name, button))
            except Exception as e:
                logger.warning(f"Erreur traitement produit: {str(e)}")
                continue

        # Sélection des produits
        time.sleep(0.5)
        self._select_product(spf50_products, "SPF-50")
        time.sleep(0.5)
        self._select_product(spf30_products, "SPF-30")

        # Accès au panier
        time.sleep(0.5)
        self.click(self.CART_BUTTON, "Bouton panier")

    def _select_product(self, products, product_type):
        logger.info(f"{len(products)} produits {product_type} trouvés")
        assert len(products) > 0, f"Aucun produit {product_type} trouvé"

        min_product = min(products, key=lambda x: x[0])
        min_product[2].click()
        logger.info(f"{product_type} sélectionné: {min_product[1]} - {min_product[0]}")

    @staticmethod
    def _extract_spf(product_name):
        match = re.search(r'SPF-(\d+)', product_name)
        return match.group(1) if match else "0"