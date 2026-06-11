from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.username_field = (By.ID, "user-name")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "login-button")

    def enter_username(self, username):
        username_field = self.wait.until(
            EC.presence_of_element_located(self.username_field)
        )
        username_field.send_keys(username)

    def enter_password(self, password):
        password_field = self.driver.find_element(*self.password_field)
        password_field.send_keys(password)

    def click_login(self):
        login_button = self.driver.find_element(*self.login_button)
        login_button.click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()