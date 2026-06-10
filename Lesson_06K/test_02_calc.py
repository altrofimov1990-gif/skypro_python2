import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestCalculator:
    def setup_method(self):
        """Инициализация драйвера Chrome перед каждым тестом"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def teardown_method(self):
        """Закрытие драйвера после каждого теста"""
        self.driver.quit()

    def test_calculator_with_delay(self):
        """
        Автотест для проверки работы калькулятора с задержкой
        """
        # Открываем страницу калькулятора
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")

        # Ожидание и ввод значения задержки в поле #delay
        delay_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#delay"))
        )
        delay_input.clear()
        delay_input.send_keys("45")

        # Нажатие на кнопки калькулятора
        buttons_to_click = ["7", "+", "8", "="]

        for button_text in buttons_to_click:
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[text()='{button_text}']"))
            )
            button.click()

        # Ожидание результата в течение 45 секунд (с запасом — 50 секунд)
        result_element = WebDriverWait(self.driver, 50).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".screen"), "15")
        )

        # Проверка результата
        result_text = self.driver.find_element(By.CSS_SELECTOR, ".screen").text
        assert result_text == "15", f"Ожидаемый результат: 15, фактический: {result_text}"

if __name__ == "__main__":
    pytest.main()