"""Базовый Page Object: явные ожидания вместо time.sleep()."""
from typing import Any, Tuple

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

Locator = Tuple[str, str]


class BasePage:
    """Общие методы работы с элементами через явные ожидания."""

    def __init__(self, driver: WebDriver, timeout: int = 15) -> None:
        self.driver: WebDriver = driver
        self.timeout: int = timeout
        self.wait: WebDriverWait = WebDriverWait(driver, timeout)

    def find(self, locator: Locator) -> Any:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator: Locator) -> None:
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator: Locator, text: str) -> None:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.clear()
        element.send_keys(text)

    def is_visible(self, locator: Locator, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False