from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from selenium.webdriver.common.by import By
import time
import allure
from utils.logger import logger


class PaymentPage(BasePage):
    IFRAME = (By.CSS_SELECTOR, "iframe.stripe_checkout_app")
    EMAIL_FIELD = (By.CSS_SELECTOR, "input#email")
    CARD_FIELD = (By.ID, "card_number")
    EXPIRY_FIELD = (By.ID, "cc-exp")
    CVV_FIELD = (By.ID, "cc-csc")
    ZIP_FIELD = (By.ID, "billing-zip")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    RESULT_HEADER = (By.XPATH, "//h2[contains(., 'PAYMENT')]")

    def fill_payment_form(self, email, card_number, expiry, cvv, zip_code):
        time.sleep(0.5)
        # Passer à l'iframe
        iframe = self.wait.until(EC.presence_of_element_located(self.IFRAME))
        self.driver.switch_to.frame(iframe)
        time.sleep(0.5)
        # Remplir les champs
        self._fill_field(self.EMAIL_FIELD, email, "Email")
        self._fill_card_field(card_number)
        self._fill_expiry_field(expiry)
        self._fill_field(self.CVV_FIELD, cvv, "CVV")
        self._fill_field(self.ZIP_FIELD, zip_code, "Code postal")

        # Soumettre
        self.click(self.SUBMIT_BUTTON, "Bouton de soumission")
        allure.attach(
            f"Paiement avec:\nEmail: {email}\nCarte: {card_number}\nExp: {expiry}\nCVV: {cvv}\nCode postal: {zip_code}",
            name="Détails paiement",
            attachment_type=allure.attachment_type.TEXT
        )


        # Revenir au contexte principal
        self.driver.switch_to.default_content()

    def verify_payment_result(self):
        result_header = self.get_text(self.RESULT_HEADER, "Résultat paiement")
        assert "SUCCESS" in result_header, f"Échec du paiement! Statut: {result_header}"
        logger.info("Paiement réussi")

    def _fill_field(self, locator, value, description):
        self.send_keys(locator, value, description)
        time.sleep(0.3)

    def _fill_card_field(self, card_number):
        field = self.wait.until(EC.element_to_be_clickable(self.CARD_FIELD))
        for digit in card_number:
            field.send_keys(digit)
            time.sleep(0.3)

    def _fill_expiry_field(self, expiry):
        month, year = expiry.split('/')
        field = self.wait.until(EC.element_to_be_clickable(self.EXPIRY_FIELD))
        field.send_keys(month)
        time.sleep(0.3)
        field.send_keys(year)
        time.sleep(0.3)