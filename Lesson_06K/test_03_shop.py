import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class TestShopPurchase:
    @pytest.fixture(autouse=True)
    def setup(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")

        self.driver = webdriver.Firefox(options=options)
        self.wait = WebDriverWait(self.driver, 15)  # Увеличено время ожидания до 15 с
        yield
        self.driver.quit()

    def test_purchase_items(self):
        """
        Автотест покупки товаров в интернет‑магазине
        """
        try:
            # Шаг 1: Открытие сайта магазина
            self.driver.get("https://www.saucedemo.com/")  # Исправлен URL

            # Шаг 2: Авторизация как пользователь standard_user
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "user-name"))
            )
            username_field.send_keys("standard_user")

            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys("secret_sauce")

            login_button = self.driver.find_element(By.ID, "login-button")
            login_button.click()

            # Дополнительная проверка успешной авторизации
            self.wait.until(EC.url_contains("inventory"))

            # Шаг 3: Добавление товаров в корзину
            # Sauce Labs Backpack — используем более надёжный селектор
            backpack_add_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                    "//div[contains(text(), 'Sauce Labs Backpack')]/following::button[contains(text(), 'Add to cart')]"))
            )
            backpack_add_button.click()

            # Sauce Labs Bolt T‑Shirt
            tshirt_add_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
            "//div[contains(text(), 'Sauce Labs Bolt T-Shirt')]/following::button[contains(text(), 'Add to cart')]"))
            )
            tshirt_add_button.click()

            # Sauce Labs Onesie
            onesie_add_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
            "//div[contains(text(), 'Sauce Labs Onesie')]/following::button[contains(text(), 'Add to cart')]"))
            )
            onesie_add_button.click()

            # Шаг 4: Переход в корзину
            cart_link = self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
            )
            cart_link.click()

            # Шаг 5: Нажатие Checkout
            checkout_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "checkout"))
            )
            checkout_button.click()

            # Шаг 6: Заполнение формы своими данными
            first_name_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "first-name"))
            )
            first_name_field.send_keys("Иван")

            last_name_field = self.driver.find_element(By.ID, "last-name")
            last_name_field.send_keys("Иванов")

            postal_code_field = self.driver.find_element(By.ID, "postal-code")
            postal_code_field.send_keys("123456")

            # Шаг 7: Нажатие кнопки Continue
            continue_button = self.driver.find_element(By.ID, "continue")
            continue_button.click()

            # Шаг 8: Чтение итоговой стоимости (Total)
            total_element = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label"))
            )
            total_text = total_element.text
            # Извлекаем числовую часть из строки вида "Total: $58.29"
            total_amount = float(total_text.split("$")[1])

            # Шаг 9: Проверка итоговой суммы
            expected_total = 58.29
            assert total_amount == expected_total, f"Ожидаемая сумма {expected_total}, но получена {total_amount}"

        except TimeoutException as e:
            pytest.fail(f"Таймаут ожидания элемента: {e}")
        except Exception as e:
            pytest.fail(f"Произошла ошибка во время теста: {e}")