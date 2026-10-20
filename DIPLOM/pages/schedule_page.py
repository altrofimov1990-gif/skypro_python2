"""Page Object страницы «Расписание» кабинета учителя Skyeng.

Локаторы приведены как базовые: сверьте их со своей сборкой интерфейса
через DevTools (ПКМ -> Просмотреть код), тег data-testid и классы могут отличаться.
"""
from typing import Tuple

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config import SCHEDULE_PATH
from pages.base_page import BasePage, Locator
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class SchedulePage(BasePage):
    CREATE_BUTTON: Tuple[str, str] = (By.XPATH, '//button[contains(., "Создать") or contains(., "событие")]')
    TITLE_INPUT: Tuple[str, str] = (By.CSS_SELECTOR, 'input[name="title"], input[placeholder*="названи" i]')
    SAVE_BUTTON: Tuple[str, str] = (By.XPATH, '//button[contains(., "Сохранить")]')
    DELETE_BUTTON: Tuple[str, str] = (By.XPATH, '//button[contains(., "Удалить")]')
    EDIT_BUTTON: Tuple[str, str] = (By.XPATH, '//button[contains(., "Редактировать") or contains(., "Изменить")]')
    NEXT_WEEK_BUTTON: Tuple[str, str] = (By.XPATH, '//*[@aria-label="Следующая неделя" or contains(@class, "next")]')
    PREV_WEEK_BUTTON: Tuple[str, str] = (By.XPATH, '//*[@aria-label="Прошлая неделя" or contains(@class, "prev")]')

    def __init__(self, driver):
        super().__init__(driver)

    def open(self) -> "SchedulePage":
        with allure.step("Открыть страницу «Расписание»"):
            self.driver.get(self.driver.current_url.split("/#")[0] + SCHEDULE_PATH)
        return self

    def is_open(self) -> bool:
        return self.is_visible(("xpath", '//h1|//h2|//*[contains(@class, "schedule")]'), timeout=10)

    def create_event(self, title: str) -> None:
        self.click(self.CREATE_BUTTON)
        self.type_text(self.TITLE_INPUT, title)
        self.click(self.SAVE_BUTTON)

    def open_event(self, title):
        logging.info(f"Trying to open event: {title}")
        self.wait.until(EC.presence_of_element_located(self.EVENT_LIST))
        self.wait.until(EC.element_to_be_clickable(self.event_locator(title)))
        self.click(self.event_locator(title))

    def event_locator(self, title):
        return ('xpath', f"//div[contains(text(), '{title}')]")

    def has_event(self, title: str) -> bool:
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.event_locator(title))
            )
            return True
        except TimeoutException:
            return False

    def open_event(self, title: str) -> None:
        self.click(self.event_locator(title))

    def edit_event_title(self, old_title: str, new_title: str) -> None:
        self.open_event(old_title)
        self.click(self.EDIT_BUTTON)
        self.type_text(self.TITLE_INPUT, new_title)
        self.click(self.SAVE_BUTTON)

    def delete_event(self, title: str) -> None:
        self.open_event(title)
        self.click(self.DELETE_BUTTON)

    def switch_week(self, forward: bool = True) -> None:
        self.click(self.NEXT_WEEK_BUTTON if forward else self.PREV_WEEK_BUTTON)