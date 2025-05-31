import pytest
import allure
import time
from pages.home_page import HomePage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.payment_page import PaymentPage
from utils.database import Database
from utils.config import Config
from utils.logger import logger


@allure.feature("Weathershopper Test")
@allure.story("Comportement basé sur la température")
class TestWeathershopper:
    @allure.title("Test d'achat basé sur la température")
    def test_weathershopper_current_temperature(self, browser):
        # 1. Accéder à la page d'accueil
        with allure.step("Accéder à la page d'accueil"):
            home_page = HomePage(browser)
            browser.get(Config.BASE_URL)
            logger.info(f"Accès à l'URL: {Config.BASE_URL}")
            allure.attach(
                browser.get_screenshot_as_png(),
                name="Homepage",
                attachment_type=allure.attachment_type.PNG
            )


        # 2. Lire la température
        with allure.step("Lire la température"):
            time.sleep(0.5)
            temperature = home_page.get_temperature()
            logger.info(f"Température détectée: {temperature}°C")
            allure.attach(
                f"Température actuelle: {temperature}°C",
                name="Température",
                attachment_type=allure.attachment_type.TEXT
            )

        # 3. Récupérer les données de paiement
        with allure.step("Récupérer les données de paiement"):
            payment_data = Database.get_random_payment()
            logger.info(f"Données de paiement récupérées: {payment_data[0]}")

        # 4. Sélectionner les produits
        if temperature < 19:
            time.sleep(0.5)
            with allure.step("Acheter des moisturizers"):
                home_page.click_buy_moisturizers()

                # Capture d'écran de la page des moisturizers
                allure.attach(
                    browser.get_screenshot_as_png(),
                    name="Moisturizers_Page",
                    attachment_type=allure.attachment_type.PNG
                )

                products_page = ProductsPage(browser)
                time.sleep(0.5)
                products_page.add_moisturizers()
        elif temperature > 34:
            time.sleep(0.5)
            with allure.step("Acheter des sunscreens"):
                home_page.click_buy_sunscreens()

                # Capture d'écran de la page des sunscreens
                allure.attach(
                    browser.get_screenshot_as_png(),
                    name="Sunscreens_Page",
                    attachment_type=allure.attachment_type.PNG
                )

                products_page = ProductsPage(browser)
                time.sleep(0.5)
                products_page.add_sunscreens()
        else:
            logger.info("Température modérée - Aucune action nécessaire")
            pytest.skip("La température est comprise entre 19 et 34°C - Aucune action requise")

        time.sleep(0.5)
        # 5. Vérifier le panier
        with allure.step("Vérifier le panier"):
            cart_page = CartPage(browser)
            cart_page.verify_cart()

            # Capture d'écran du panier
            allure.attach(
                browser.get_screenshot_as_png(),
                name="Cart_Page",
                attachment_type=allure.attachment_type.PNG
            )
        time.sleep(0.5)
        cart_page.proceed_to_payment()

        # 6. Remplir le formulaire de paiement
        with allure.step("Remplir le formulaire de paiement"):
            payment_page = PaymentPage(browser)
            time.sleep(0.5)
            payment_page.fill_payment_form(*payment_data)
            allure.attach(
                browser.get_screenshot_as_png(),
                name="Formulaire_paiement",
                attachment_type=allure.attachment_type.PNG
            )
        # 7. Vérifier le résultat
        with allure.step("Vérifier le résultat du paiement"):
            # Ajouter un délai pour permettre à la page de résultat de s'afficher
            time.sleep(3)
            payment_page.verify_payment_result()
            # Capture d'écran du résultat
            allure.attach(
                browser.get_screenshot_as_png(),
                name="Payment_Result",
                attachment_type=allure.attachment_type.PNG
            )

