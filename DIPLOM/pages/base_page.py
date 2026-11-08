# pages/base_page.py
"""Базовый Page Object с общими методами работы с элементами."""
import logging
from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

Locator = Tuple[str, str]


class BasePage:
    """Хранит драйвер и предоставляет общие действия над страницей."""

    def __init__(self, driver: WebDriver) -> None:
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, 10)
        logging.info("BasePage initialized")

    def click(self, locator: Locator) -> None:
        """Кликает по элементу, дожидаясь его кликабельности."""
        logging.info("Trying to click: %s", locator)
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
