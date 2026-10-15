from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class CalculatorPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Локаторы элементов
    DELAY_INPUT = (By.CSS_SELECTOR, "#delay")
    SCREEN = (By.CSS_SELECTOR, ".screen")

    def open(self, url):
        """Открыть страницу калькулятора"""
        self.driver.get(url)

    def set_delay(self, delay_value):
        """Установить значение задержки в поле #delay"""
        delay_input = self.wait.until(
            EC.presence_of_element_located(self.DELAY_INPUT)
        )
        delay_input.clear()
        delay_input.send_keys(str(delay_value))

    def click_button(self, button_text):
        """Нажать на кнопку калькулятора по тексту"""
        button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//span[text()='{button_text}']"))
        )
        button.click()

    def get_result(self):
        """Получить текущий результат из экрана калькулятора"""
        result_element = self.wait.until(
            EC.visibility_of_element_located(self.SCREEN)
        )
        return result_element.text

    def wait_for_result(self, expected_result, timeout=45):
        """Ожидать появления ожидаемого результата"""
        self.wait = WebDriverWait(self.driver, timeout)
        self.wait.until(
            EC.text_to_be_present_in_element(self.SCREEN, str(expected_result))
        )