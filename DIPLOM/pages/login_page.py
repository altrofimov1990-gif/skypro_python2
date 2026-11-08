# pages/login_page.py
"""Page Object страницы входа id.skyeng.ru (вход по одноразовому коду)."""
import logging
import time
from typing import Tuple

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import AUTH_CODE, LOGIN_EMAIL
from pages.base_page import BasePage

Locator = Tuple[str, str]


class LoginPage(BasePage):
    """Форма входа Skyeng ID: email/телефон -> одноразовый код."""

    URL: str = "https://id.skyeng.ru/"

    IDENTITY_INPUT: Locator = (By.NAME, "identity")
    GET_CODE_BUTTON: Locator = (
        By.XPATH, '//button[contains(., "Получить код")]',
    )
    AGREEMENT_CHECKBOX: Locator = (
        By.CSS_SELECTOR,
        "input[type='checkbox'].js-register-by-socials-terms-agreement",
    )
    SUBMIT_BUTTON: Locator = (
        By.XPATH,
        "//button[@type='submit' and contains(@class, '-type-primary')]",
    )
    CODE_INPUTS: Locator = (
        By.XPATH,
        "//input[contains(@name, 'code') or contains(@class, 'code')]",
    )

    def open(self) -> None:
        """Открывает страницу входа Skyeng ID."""
        self.driver.get(self.URL)
        self.wait.until(EC.url_contains("id.skyeng.ru"))
        time.sleep(3)
        logging.info("Login page opened: %s", self.driver.current_url)

    @allure.step("Ввести почту и запросить одноразовый код")
    def request_code(self, identity: str = "") -> None:
        """Вводит email/телефон и нажимает «Получить код»."""
        field = self.wait.until(
            EC.element_to_be_clickable(self.IDENTITY_INPUT)
        )
        field.clear()
        field.send_keys(identity or LOGIN_EMAIL)
        logging.info("Identity введён: %s", identity or LOGIN_EMAIL)
        self.driver.find_element(*self.GET_CODE_BUTTON).click()
        logging.info("Нажата кнопка «Получить код»")

    @allure.step("Подтвердить согласие с условиями, если требуется")
    def agree_if_needed(self) -> None:
        """Отмечает чекбокс согласия, если он виден и не отмечен."""
        try:
            checkbox = self.driver.find_element(*self.AGREEMENT_CHECKBOX)
            if checkbox.is_displayed() and not checkbox.is_selected():
                checkbox.click()
                logging.info("Чекбокс согласия отмечен")
        except Exception:  # noqa: BLE001
            logging.info("Чекбокс согласия не найден — пропускаю")

    @allure.step("Ввести одноразовый код и войти")
    def enter_code(self, code: str = "") -> None:
        """Вводит одноразовый код и отправляет форму входа."""
        inputs = self.driver.find_elements(*self.CODE_INPUTS)
        if not inputs:
            self.log_page_state()
            raise AssertionError("Поля для кода не найдены")
        value = code or AUTH_CODE
        if len(inputs) > 1:
            for index, field in enumerate(inputs[: len(value)]):
                field.send_keys(value[index])
        else:
            inputs[0].send_keys(value)
        logging.info("Код введён (%d символов)", len(value))
        try:
            self.wait.until(
                EC.element_to_be_clickable(self.SUBMIT_BUTTON)
            ).click()
            logging.info("Нажата кнопка входа")
        except TimeoutException:
            logging.info("Кнопка входа не найдена — форма отправилась сама")

    @allure.step("Дождаться входа в кабинет")
    def wait_logged_in(self, timeout: int = 30) -> None:
        """Ждёт перехода в кабинет учителя после входа."""
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            if "teachers.skyeng.ru" in self.driver.current_url:
                logging.info("Вход выполнен: %s", self.driver.current_url)
                return
            time.sleep(1)
        raise AssertionError(
            f"Вход не выполнен за {timeout} секунд, текущий URL: "
            f"{self.driver.current_url}"
        )

    @allure.step("Полный вход по одноразовому коду")
    def login(self, identity: str = "", code: str = "") -> None:
        """Полный сценарий входа: email -> код -> кабинет."""
        self.open()
        self.request_code(identity)
        self.agree_if_needed()
        self.enter_code(code)
        self.wait_logged_in()
