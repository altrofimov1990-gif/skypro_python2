import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

class TestShopPurchaseWithPageObject:
    @pytest.fixture(autouse=True)
    def setup(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")

        self.driver = webdriver.Firefox(options=options)
        yield
        self.driver.quit()

    def test_purchase_items_with_page_object(self):
        """
        Автотест покупки товаров в интернет‑магазине с использованием Page Object
        """
        try:
            # Шаг 1: Открытие сайта магазина
            self.driver.get("https://www.saucedemo.com/")

            # Создаём объекты страниц
            login_page = LoginPage(self.driver)
            inventory_page = InventoryPage(self.driver)
            cart_page = CartPage(self.driver)
            checkout_page = CheckoutPage(self.driver)

            # Шаг 2: Авторизация как пользователь standard_user
            login_page.login("standard_user", "secret_sauce")

            # Дополнительная проверка успешной авторизации
            wait = WebDriverWait(self.driver, 15)
            wait.until(lambda driver: "inventory" in driver.current_url)

            # Шаг 3: Добавление товаров в корзину
            inventory_page.add_backpack_to_cart()
            inventory_page.add_tshirt_to_cart()
            inventory_page.add_onesie_to_cart()

            # Шаг 4: Переход в корзину
            inventory_page.go_to_cart()

            # Шаг 5: Нажатие Checkout
            cart_page.proceed_to_checkout()

            # Шаг 6: Заполнение формы своими данными
            checkout_page.fill_personal_info("Иван", "Иванов", "123456")

            # Шаг 7: Нажатие кнопки Continue
            checkout_page.continue_checkout()

            # Шаг 8: Чтение итоговой стоимости (Total)
            total_amount = checkout_page.get_total_amount()

            # Шаг 9: Проверка итоговой суммы
            expected_total = 58.29
            assert total_amount == expected_total, f"Ожидаемая сумма {expected_total}, но получена {total_amount}"

        except TimeoutException as e:
            pytest.fail(f"Таймаут ожидания элемента: {e}")
        except Exception as e:
            pytest.fail(f"Произошла ошибка во время теста: {e}")