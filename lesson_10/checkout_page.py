import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    """Страница оформления заказа."""

    def __init__(self, driver) -> None:
        """
        Инициализация страницы оформления.

        :param driver: экземпляр WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.first_name_field = (By.ID, "first-name")
        self.last_name_field = (By.ID, "last-name")
        self.postal_code_field = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.total_label = (By.CLASS_NAME, "summary_total_label")

    @allure.step("Заполнение личных данных: имя, фамилия, почтовый индекс")
    def fill_personal_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        """
        Заполнить поля формы личными данными.

        :param first_name: имя
        :param last_name: фамилия
        :param postal_code: почтовый индекс
        :return: None
        """
        first_name_field = self.wait.until(
            EC.presence_of_element_located(self.first_name_field)
        )
        first_name_field.send_keys(first_name)

        last_name_field = self.driver.find_element(*self.last_name_field)
        last_name_field.send_keys(last_name)

        postal_code_field = self.driver.find_element(*self.postal_code_field)
        postal_code_field.send_keys(postal_code)

    @allure.step("Нажатие кнопки Continue")
    def continue_checkout(self) -> None:
        """
        Продолжить оформление заказа.

        :return: None
        """
        continue_button = self.driver.find_element(*self.continue_button)
        continue_button.click()

    @allure.step("Получение итоговой суммы заказа")
    def get_total_amount(self) -> float:
        """
        Получить итоговую сумму заказа со страницы.

        :return: сумма заказа в виде float
        """
        total_element = self.wait.until(
            EC.presence_of_element_located(self.total_label)
        )
        total_text = total_element.text
        total_amount = float(total_text.split("$")[1])
        return total_amount