from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    """Страница корзины в интернет-магазине."""

    def __init__(self, driver) -> None:
        """
        Инициализация страницы корзины.

        :param driver: экземпляр WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.checkout_button = (By.ID, "checkout")

    def proceed_to_checkout(self) -> None:
        """
        Перейти к оформлению заказа, нажав кнопку Checkout.

        :return: None
        """
        checkout_button = self.wait.until(
            EC.element_to_be_clickable(self.checkout_button)
        )
        checkout_button.click()