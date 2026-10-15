from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.checkout_button = (By.ID, "checkout")

    def proceed_to_checkout(self):  # Исправлено: proceed → proceed
        checkout_button = self.wait.until(
            EC.element_to_be_clickable(self.checkout_button)
        )
        checkout_button.click()