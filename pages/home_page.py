from .base_page import BasePage
from selenium.webdriver.common.by import By
import re



class HomePage(BasePage):
    TEMPERATURE = (By.ID, "temperature")
    BUY_MOISTURIZERS_BTN = (By.XPATH, "//button[text()='Buy moisturizers']")
    BUY_SUNSCREENS_BTN = (By.XPATH, "//button[text()='Buy sunscreens']")

    def get_temperature(self):
        temp_text = self.get_text(self.TEMPERATURE, "Température")
        return int(re.search(r'\d+', temp_text).group())

    def click_buy_moisturizers(self):
        self.click(self.BUY_MOISTURIZERS_BTN, "Bouton Buy moisturizers")

    def click_buy_sunscreens(self):
        self.click(self.BUY_SUNSCREENS_BTN, "Bouton Buy sunscreens")