from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

        # Чёткие имена: _input для полей ввода
        self.username_input = (By.ID, "user-name")
        self.password_input = (By.ID, "password")
        self.login_button = (By.CSS_SELECTOR, ".btn_action")

    def login(self, username, password):
        # Если вдруг не на той странице — переходим
        if "saucedemo.com" not in self.driver.current_url:
            self.driver.get("https://www.saucedemo.com/")

        # Ввод логина
        user_field = self.wait.until(
            EC.visibility_of_element_located(self.username_input)
        )
        user_field.clear()
        user_field.send_keys(username)

        # Ввод пароля
        pass_field = self.wait.until(
            EC.visibility_of_element_located(self.password_input)
        )
        pass_field.clear()
        pass_field.send_keys(password)

        # Клик по кнопке
        btn = self.wait.until(
            EC.element_to_be_clickable(self.login_button)
        )
        btn.click()