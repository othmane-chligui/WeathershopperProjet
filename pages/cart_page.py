from .base_page import BasePage
from selenium.webdriver.common.by import By


class CartPage(BasePage):
    CART_ITEMS = (By.XPATH, "//tbody/tr")
    PAY_BUTTON = (By.XPATH, "//span[text()='Pay with Card']")
    CHECKOUT_HEADER = (By.XPATH, "//h2[contains(text(), 'Checkout')]")

    def verify_cart(self):
        self.is_visible(self.CHECKOUT_HEADER, "En-tête Checkout")
        cart_items = self.driver.find_elements(*self.CART_ITEMS)
        assert len(cart_items) == 2, f"Attendu 2 articles, trouvé {len(cart_items)}"
        return cart_items

    def proceed_to_payment(self):
        self.click(self.PAY_BUTTON, "Bouton Pay with Card")