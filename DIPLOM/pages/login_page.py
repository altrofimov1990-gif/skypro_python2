"""Page Object страницы входа id.skyeng.ru (вход по одноразовому коду)."""
from typing import Any, Tuple

import allure
import pytest
from selenium.webdriver.common.by import By

from config import AUTH_CODE
from pages.base_page import BasePage, Locator


class LoginPage(BasePage):
    """Форма входа Skyeng ID: email/телефон -> одноразовый код."""

    IDENTITY_INPUT: Tuple[str, str] = (By.NAME, "identity")
    GET_CODE_BUTTON: Tuple[str, str] = (
        By.XPATH, '//button[contains(., "Получить код")]',
    )
    AGREEMENT_CHECKBOX: Tuple[str, str] = (
        By.CSS_SELECTOR, "input[type='checkbox'].js-register-by-socials-terms-agreement",
    )
    SUBMIT_BUTTON: Tuple[str, str] = (
        By.XPATH, "//button[@type='submit' and contains(@class, 'button--primary')]",
    )

    def open(self) -> "LoginPage":
        with allure.step("Открыть страницу входа Skyeng ID"):
            self.driver.get("https://id.skyeng.ru/login")
        return self

    def request_code(self, identity: str) -> None:
        with allure.step("Ввести почту/телефон и запросить код"):
            self.type_text(self.IDENTITY_INPUT, identity)
            self.click(self.GET_CODE_BUTTON)

    def enter_code_and_submit(self, code: str) -> None:
        with allure.step("Ввести одноразовый код и подтвердить вход"):
            code_input: Locator = (By.CSS_SELECTOR, "input.js-send-otp-form-input")
            self.type_text(code_input, code)
            self.click(self.SUBMIT_BUTTON)

    def is_logged_in(self) -> bool:
        """Вход успешен, если страница больше не formа входа."""
        url: str = self.driver.current_url
        return "id.skyeng.ru/login" not in url

    def login(self, email: str, password: str) -> None:
        """Совместим с сигнатурой теста. Пароль не используется:
        форма входа Skyeng работает по одноразовому коду."""
        self.request_code(email)
        code: str = AUTH_CODE
        if not code:
            pytest.skip(
                "Форма входа использует одноразовый код, а не пароль. "
                "Для полного UI-логина добавьте AUTH_CODE в .env; "
                "иначе тест пропускается, а авторизация идёт через cookie."
            )
        self.enter_code_and_submit(code)