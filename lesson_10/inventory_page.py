import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    """Страница каталога товаров."""

    def __init__(self, driver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

        self.backpack_add_button = (
            By.XPATH,
            "//div[contains(@class, 'inventory_item') and .//*[contains(text(), 'Sauce Labs Backpack')]]//button[contains(text(), 'Add to cart')]"
        )
        self.tshirt_add_button = (
            By.XPATH,
            "//div[contains(@class, 'inventory_item') and .//*[contains(text(), 'Sauce Labs Bolt T-Shirt')]]//button[contains(text(), 'Add to cart')]"
        )
        self.onesie_add_button = (
            By.XPATH,
            "//div[contains(@class, 'inventory_item') and .//*[contains(text(), 'Sauce Labs Onesie')]]//button[contains(text(), 'Add to cart')]"
        )
        self.cart_link = (By.CLASS_NAME, "shopping_cart_link")

    @allure.step("Дождаться загрузки страницы каталога")
    def wait_for_page_loaded(self) -> None:
        """Ждёт, пока на странице появится хотя бы одна карточка товара."""
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
        )

    @allure.step("Добавить рюкзак в корзину")
    def add_backpack_to_cart(self) -> None:
        backpack_button = self.wait.until(
            EC.element_to_be_clickable(self.backpack_add_button)
        )
        backpack_button.click()

    @allure.step("Перейти в корзину")
    def go_to_cart(self) -> None:
        cart_link = self.wait.until(
            EC.element_to_be_clickable(self.cart_link)
        )
        cart_link.click()