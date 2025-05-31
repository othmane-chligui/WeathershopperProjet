from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import logger
import allure
from utils.config import Config


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.WAIT_TIMEOUT)
        self.logger = logger

    def click(self, locator, description=""):
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.info(f"Clique sur {description}")
        except TimeoutException:
            self.logger.error(f"Élément non cliquable: {description}")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=f"Erreur_click_{description}",
                attachment_type=allure.attachment_type.PNG
            )
            raise

    def send_keys(self, locator, text, description=""):
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)
            self.logger.info(f"Texte entré dans {description}: {text}")
        except TimeoutException:
            self.logger.error(f"Élément non visible: {description}")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=f"Erreur_sendkeys_{description}",
                attachment_type=allure.attachment_type.PNG
            )
            raise

    def get_text(self, locator, description=""):
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            text = element.text
            self.logger.info(f"Texte récupéré de {description}: {text}")
            return text
        except TimeoutException:
            self.logger.error(f"Élément non visible: {description}")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=f"Erreur_gettext_{description}",
                attachment_type=allure.attachment_type.PNG
            )
            raise

    def is_visible(self, locator, description=""):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            self.logger.info(f"Élément visible: {description}")
            return True
        except TimeoutException:
            self.logger.error(f"Élément non visible: {description}")
            return False

