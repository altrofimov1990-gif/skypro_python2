import pytest

from Lesson_07.Auto_test_1.calculator_page import CalculatorPage

class TestCalculator:
    @pytest.mark.usefixtures("driver")
    def test_calculator_with_delay(self, driver):
        """
        Автотест для проверки работы калькулятора с задержкой
        """
        # Создаём объект страницы калькулятора
        calculator_page = CalculatorPage(driver)

        # Открываем страницу калькулятора
        calculator_page.open("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")

        # Устанавливаем задержку 45 секунд
        calculator_page.set_delay(45)

        # Нажимаем кнопки калькулятора
        buttons_to_click = ["7", "+", "8", "="]
        for button_text in buttons_to_click:
            calculator_page.click_button(button_text)

        # Ждём результата и проверяем его
        calculator_page.wait_for_result("15", timeout=45)
        result = calculator_page.get_result()

        # Проверка результата (единственная assert в тесте)
        assert result == "15", f"Ожидаемый результат: 15, фактический: {result}"