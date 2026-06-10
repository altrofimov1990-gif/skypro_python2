import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestDataTypesForm(unittest.TestCase):

    def setUp(self):
        """Настройка драйвера перед каждым тестом"""
        self.driver = webdriver.Edge()  # или webdriver.Chrome(), в зависимости от вашего браузера
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        """Закрытие драйвера после каждого теста"""
        self.driver.quit()

    def test_form_validation(self):
        """Тест валидации формы с проверкой подсветки поля Zip code"""
        # Открытие страницы (исправлен URL: https:// → https://)
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")

        # Заполнение формы
        self.wait.until(EC.presence_of_element_located((By.NAME, "first-name"))).send_keys("Иван")
        self.wait.until(EC.presence_of_element_located((By.NAME, "last-name"))).send_keys("Петров")
        self.wait.until(EC.presence_of_element_located((By.NAME, "address"))).send_keys("Ленина, 55-3")
        self.wait.until(EC.presence_of_element_located((By.NAME, "e-mail"))).send_keys("test@skypro.com")
        self.wait.until(EC.presence_of_element_located((By.NAME, "phone"))).send_keys("+7985899998787")

        # Zip code оставляем пустым
        zip_code_field = self.wait.until(
            EC.presence_of_element_located((By.NAME, "zip-code"))
        )
        zip_code_field.clear()

        self.wait.until(EC.presence_of_element_located((By.NAME, "city"))).send_keys("Москва")
        self.wait.until(EC.presence_of_element_located((By.NAME, "country"))).send_keys("Россия")
        self.wait.until(EC.presence_of_element_located((By.NAME, "job-position"))).send_keys("QA")
        self.wait.until(EC.presence_of_element_located((By.NAME, "company"))).send_keys("SkyPro")

        # Нажатие кнопки Submit
        submit_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        submit_button.click()

        # Проверка валидации полей
        try:
            # Вариант 1: пытаемся найти поле zip-code и проверить его класс
            zip_code_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "zip-code"))
            )
            # Проверяем, что у поля есть класс alert-danger (подсветка красным)
            field_class = zip_code_field.get_attribute("class")
            self.assertIn("alert-danger", field_class, "Поле Zip code не подсвечено красным")

        except TimeoutException:
            # Вариант 2: если поле исчезло, ищем сообщение об ошибке
            error_msg = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
            )
            self.assertTrue(error_msg.is_displayed(), "Сообщение об ошибке не отображается")
            print("Поле Zip code исчезло после Submit, но найдено сообщение об ошибке")

        # Дополнительная проверка: убедимся, что остальные поля заполнены корректно
        # (опционально — можно добавить проверки для других полей)

if __name__ == "__main__":
    unittest.main()