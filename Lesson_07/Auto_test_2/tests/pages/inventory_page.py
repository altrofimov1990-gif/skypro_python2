from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.backpack_add_button = (
            By.XPATH,
            "//div[contains(text(), 'Sauce Labs Backpack')]/following::button[contains(text(), 'Add to cart')]"
        )
        self.tshirt_add_button = (
            By.XPATH,
            "//div[contains(text(), 'Sauce Labs Bolt T-Shirt')]/following::button[contains(text(), 'Add to cart')]"
        )
        self.onesie_add_button = (
            By.XPATH,
            "//div[contains(text(), 'Sauce Labs Onesie')]/following::button[contains(text(), 'Add to cart')]"
        )
        self.cart_link = (By.CLASS_NAME, "shopping_cart_link")

    def add_backpack_to_cart(self):
        backpack_button = self.wait.until(
            EC.element_to_be_clickable(self.backpack_add_button)
        )
        backpack_button.click()

    def add_tshirt_to_cart(self):
        tshirt_button = self.wait.until(
            EC.element_to_be_clickable(self.tshirt_add_button)
        )
        tshirt_button.click()

    def add_onesie_to_cart(self):
        onesie_button = self.wait.until(
            EC.element_to_be_clickable(self.onesie_add_button)
        )
        onesie_button.click()

    def go_to_cart(self):
        cart_link = self.wait.until(
            EC.element_to_be_clickable(self.cart_link)
        )
        cart_link.click()