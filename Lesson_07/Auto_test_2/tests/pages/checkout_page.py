from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.first_name_field = (By.ID, "first-name")
        self.last_name_field = (By.ID, "last-name")
        self.postal_code_field = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.total_label = (By.CLASS_NAME, "summary_total_label")

    def fill_personal_info(self, first_name, last_name, postal_code):
        first_name_field = self.wait.until(
            EC.presence_of_element_located(self.first_name_field)
        )
        first_name_field.send_keys(first_name)

        last_name_field = self.driver.find_element(*self.last_name_field)
        last_name_field.send_keys(last_name)

        postal_code_field = self.driver.find_element(*self.postal_code_field)
        postal_code_field.send_keys(postal_code)

    def continue_checkout(self):
        continue_button = self.driver.find_element(*self.continue_button)
        continue_button.click()

    def get_total_amount(self):
        total_element = self.wait.until(
            EC.presence_of_element_located(self.total_label)
        )
        total_text = total_element.text
        # Извлекаем числовую часть из строки вида "Total: $58.29"
        total_amount = float(total_text.split("$")[1])
        return total_amount