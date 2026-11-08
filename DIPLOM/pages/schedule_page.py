# pages/schedule_page.py
"""Page Object страницы расписания кабинета учителя Skyeng."""
import logging
import time
from typing import Any, List, Optional, Tuple

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

Locator = Tuple[str, str]

FIELD_XPATH: str = (
    "//input | //textarea | //*[@contenteditable='true']"
)


class SchedulePage(BasePage):
    URL: str = "https://teachers.skyeng.ru/schedule"

    SAVE_TEXTS = (
        "Сохранить", "Cохранить", "Добавить", "Создать", "Готово",
        "ОК", "OK",
    )

    PLUS_BUTTONS: List[Locator] = [
        (By.XPATH,
         "//*[contains(@class, 'plus') or contains(@class, 'add')]"
         "[self::button or self::div or self::span]"),
        (By.XPATH,
         "//*[text()='+'][self::button or self::div or self::span]"),
    ]

    CREATION_TABS: List[Locator] = [
        (By.XPATH,
         "//button[contains(normalize-space(.), 'Личное событие')]"),
        (By.XPATH,
         "//*[@role='dialog']//button"
         "[contains(normalize-space(.), 'Личное')]"),
        (By.XPATH,
         "//*[contains(normalize-space(.), 'Личное событие')]"
         "[self::button or self::div or self::span]"),
    ]

    CREATE_BUTTONS: List[Locator] = [
        (By.XPATH, "//button[contains(normalize-space(.), 'Создать')]"),
        (By.XPATH, "//*[@aria-label][contains(@aria-label, 'Создать')]"),
        (By.XPATH,
         "//*[contains(@class, 'add-event')]"
         "[self::button or self::div or self::span]"),
    ]

    EDIT_BUTTONS: List[Locator] = [
        (By.XPATH, "//button[contains(normalize-space(.), 'Редактировать')]"),
        (By.XPATH, "//button[contains(normalize-space(.), 'Ред')]"),
    ]

    SAVE_BUTTONS: List[Locator] = [
        (By.XPATH, "//button[contains(normalize-space(.), 'Сохранить')]"),
        (By.XPATH,
         "//*[contains(@class, '-type-primary')]"
         "[contains(normalize-space(.), 'охранить')]"),
        (By.XPATH, "//button[contains(normalize-space(.), 'Готово')]"),
    ]

    DELETE_BUTTONS: List[Locator] = [
        (By.XPATH,
         "//*[@role='dialog']//button"
         "[contains(normalize-space(.), 'Удалить')]"),
        (By.XPATH, "//button[contains(normalize-space(.), 'Удалить')]"),
        (By.XPATH, "//*[@aria-label][contains(@aria-label, 'Удалить')]"),
    ]

    MORE_BUTTONS: List[Locator] = [
        (By.XPATH, "//*[@role='dialog']//*[contains(@class, 'cog-btn')]"),
        (By.XPATH,
         "//*[@role='dialog']//button"
         "[contains(@aria-label, 'Ещё')]"),
        (By.XPATH, "//button[contains(@aria-label, 'Ещё')]"),
        (By.XPATH,
         "//*[contains(@class, 'dots') or contains(@class, 'more')]"),
    ]

    CONFIRM_DELETE_BUTTONS: List[Locator] = [
        (By.XPATH,
         "//*[@role='dialog']//button"
         "[contains(normalize-space(.), 'Удалить')]"),
        (By.XPATH, "//button[contains(normalize-space(.), 'Да, удалить')]"),
        (By.XPATH, "//button[contains(normalize-space(.), 'Удалить')]"),
    ]

    # ------------------------------ база ------------------------------

    def open(self) -> None:
        """Открывает страницу расписания."""
        self.driver.get(self.URL)
        self.wait.until(EC.url_contains("teachers.skyeng.ru"))
        time.sleep(5)
        logging.info("Schedule page opened: %s", self.driver.current_url)

    def overlay_open(self) -> bool:
        """True, если открыт оверлей или форма с деталями события."""
        overlays = self.driver.find_elements(
            By.XPATH,
            "//*[@role='dialog'] | //div[contains(@class, 'overlay')]"
            " | //div[contains(@class, 'modal')]"
            " | //div[contains(@class, 'popup')]",
        )
        if any(element.is_displayed() for element in overlays):
            return True
        buttons = self.driver.find_elements(By.XPATH, "//button")
        for button in buttons:
            if (button.text or "").strip() in ("Сохранить", "Cохранить"):
                return True
        return False

    def _modal_open(self) -> bool:
        """True, если на странице открыт оверлей или есть поле ввода."""
        if self.overlay_open():
            return True
        return bool(
            self.driver.find_elements(By.XPATH, FIELD_XPATH)
        )

    def _click_first_available(
        self, locators: List[Locator], name: str
    ) -> None:
        """Кликает первый кликабельный элемент из списка локаторов."""
        last_error: Optional[TimeoutException] = None
        for locator in locators:
            try:
                self.wait.until(
                    EC.element_to_be_clickable(locator)
                ).click()
                logging.info(
                    "Clicked %s via %s", name, str(locator[1])[:60]
                )
                return
            except TimeoutException as error:
                last_error = error
        self.log_page_state()
        raise AssertionError(f"Не найден элемент: {name}") from last_error

    def _click_robust(self, element: Any) -> None:
        """Кликает элемент, а при перехвате клика — через JavaScript."""
        try:
            element.click()
        except ElementClickInterceptedException:
            logging.info("Клик перехвачен плашкой — кликаю через JS")
            self.driver.execute_script("arguments[0].click();", element)

    def _click_real(self, element: Any) -> None:
        """Кликает по элементу настоящими событиями мыши.

        JS-клик Angular-интерфейс иногда молча не обрабатывает,
        поэтому вкладки и кнопки форм жмём настоящей мышью.
        """
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        try:
            action = ActionChains(self.driver)
            action.move_to_element(element).click().perform()
        except WebDriverException:
            logging.info("Реальный клик не удался — кликаю через JS")
            self.driver.execute_script("arguments[0].click();", element)

    def log_page_state(self) -> None:
        """Логирует первые кнопки и поля на странице для диагностики."""
        elements = self.driver.find_elements(
            By.XPATH,
            "//button | //*[@role='button'] | //*[@contenteditable='true']",
        )
        shown: List[str] = []
        for element in elements[:10]:
            shown.append(
                f"text='{(element.text or '').strip()[:30]}' "
                f"class='{(element.get_attribute('class') or '')[:50]}'"
            )
        logging.info("Buttons on page: %s", "; ".join(shown))

    def _log_buttons_detail(self) -> None:
        """Подробный дамп кнопок: текст, aria-label, класс, внутри ли диалога."""
        elements = self.driver.find_elements(By.XPATH, "//button")
        dialogs = self.driver.find_elements(By.XPATH, "//*[@role='dialog']")
        for element in elements[:15]:
            inside = any(
                self._contains(dialog, element) for dialog in dialogs
            )
            logging.info(
                "BTN text='%s' aria='%s' class='%s' in_dialog=%s",
                (element.text or "").strip()[:40],
                (element.get_attribute("aria-label") or "")[:30],
                (element.get_attribute("class") or "")[:60],
                inside,
            )

    # --------------------- сохранение формы ---------------------

    def _find_save_button(self) -> Optional[Any]:
        """Видимая кнопка сохранения: сначала внутри диалога, потом по странице."""
        prefixes = ("//*[@role='dialog']//", "//")
        for prefix in prefixes:
            for text in self.SAVE_TEXTS:
                buttons = self.driver.find_elements(
                    By.XPATH,
                    f"{prefix}button[contains(normalize-space(.), '{text}')]",
                )
                for button in buttons:
                    if button.is_displayed():
                        logging.info(
                            "Найдена кнопка сохранения: '%s' enabled=%s "
                            "scope=%s",
                            (button.text or "").strip(),
                            button.is_enabled(),
                            "dialog" if prefix.startswith("//*") else "page",
                        )
                        return button
            buttons = self.driver.find_elements(
                By.XPATH,
                f"{prefix}button[contains(@class, '-type-primary')]",
            )
            for button in buttons:
                if button.is_displayed():
                    logging.info(
                        "Кнопка сохранения по классу: '%s' enabled=%s "
                        "scope=%s",
                        (button.text or "").strip(),
                        button.is_enabled(),
                        "dialog" if prefix.startswith("//*") else "page",
                    )
                    return button
        return None

    def _edit_form_closed(self) -> bool:
        """True, если в диалогах больше нет кнопки сохранения."""
        for text in self.SAVE_TEXTS:
            buttons = self.driver.find_elements(
                By.XPATH,
                f"//button[contains(normalize-space(.), '{text}')]",
            )
            if any(button.is_displayed() for button in buttons):
                return False
        return True

    def _closed(self) -> bool:
        """True, если форма закрыта (с защитой от stale-элементов)."""
        try:
            return not self._modal_open()
        except WebDriverException:
            return True

    def _refind_field(
        self, value: str, timeout: int = 5
    ) -> Optional[Any]:
        """Ищет заново поле, содержащее переданное значение."""
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            for field in self._visible_fields():
                try:
                    if not self._is_editable_text(field):
                        continue
                    if value in self._field_value(field):
                        return field
                except WebDriverException:
                    continue
            time.sleep(1)
        return None

    def _save_form(
        self, field: Optional[Any] = None, value: str = ""
    ) -> None:
        """Сохраняет форму каскадом способов с проверкой закрытия."""
        self._log_buttons_detail()
        had_dialog_button = self._find_save_button() is not None
        button = self._find_save_button()
        if button is None:
            self.log_page_state()
            logging.info("Кнопки сохранения нет — жму Enter")
        else:
            if not button.is_enabled():
                logging.warning(
                    "Кнопка сохранения неактивна — форме не хватает "
                    "обязательных полей"
                )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", button
            )
            self._click_robust(button)
            logging.info("Клик по кнопке сохранения отправлен")
        self._wait_form_done(had_dialog_button, 8)
        if self._form_done(had_dialog_button):
            logging.info("Форма закрылась после клика по кнопке")
            return
        if value:
            fresh = self._refind_field(value)
            if fresh is not None:
                try:
                    fresh.click()
                    fresh.send_keys(Keys.ENTER)
                    logging.info("Enter отправлен в заново найденное поле")
                except WebDriverException:
                    logging.info("Enter в заново найденное поле не удался")
                self._wait_form_done(had_dialog_button, 8)
                if self._form_done(had_dialog_button):
                    return
            else:
                logging.info("Поле с новым значением заново не найдено")
        retry = self._find_save_button()
        if retry is not None:
            try:
                self.driver.execute_script("arguments[0].click();", retry)
                logging.info("JS-клик по кнопке сохранения отправлен")
            except WebDriverException:
                logging.info("JS-клик по кнопке не удался")
            self._wait_form_done(had_dialog_button, 8)
            if self._form_done(had_dialog_button):
                return
        try:
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            logging.info("Реальный Enter отправлен в активный элемент")
        except WebDriverException:
            logging.warning("Реальный Enter не удался")
        self._wait_form_done(had_dialog_button, 10)
        if not self._form_done(had_dialog_button):
            self._log_form_errors()
            self.log_page_state()

    def _form_done(self, had_dialog_button: bool) -> bool:
        """True, если сохранение завершено по признакам страницы."""
        try:
            if not self._edit_form_closed():
                return False
        except WebDriverException:
            return True
        if had_dialog_button:
            return True
        return self._closed()

    def _wait_form_done(
        self, had_dialog_button: bool, timeout: int = 8
    ) -> None:
        """Ждёт завершения сохранения."""
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            if self._form_done(had_dialog_button):
                return
            time.sleep(1)
        logging.info("Форма всё ещё открыта после сохранения")

    def _log_form_errors(self) -> None:
        """Логирует текст ошибок валидации, если они показаны."""
        errors = self.driver.find_elements(
            By.XPATH,
            "//*[contains(@class, 'error') "
            "or contains(@class, 'invalid')]",
        )
        texts = [
            (element.text or "").strip()[:80]
            for element in errors
            if element.is_displayed() and (element.text or "").strip()
        ]
        if texts:
            logging.info("Ошибки формы: %s", texts)

    # --------------------- создание события ---------------------

    def create_event(self, title: str) -> None:
        """Создаёт личное событие через интерфейс.

        Если форма не открылась или вкладка «Личное событие» не
        переключилась — обновляет страницу и пробует весь поток
        ещё раз: интерфейс иногда рендерится хуже обычного.
        """
        for attempt in range(2):
            if attempt:
                logging.info("Повтор создания события (%d)", attempt + 1)
            opened = False
            try:
                self._click_first_available(
                    self.PLUS_BUTTONS, "кнопка «+»"
                )
                opened = self._modal_open()
            except AssertionError:
                logging.info("Кнопки «+» нет — пробую клик по ячейке")
            if not opened:
                try:
                    self._click_free_slot()
                except AssertionError:
                    logging.info("Ячейка не открыла форму — обновляю страницу")
                    self.driver.refresh()
                    time.sleep(5)
                    continue
            tab_ok = self._open_creation_tab()
            field = self._wait_any_field(timeout=8)
            if field is None and not tab_ok:
                logging.info(
                    "Форма не открылась — обновляю страницу и повторяю"
                )
                self.driver.refresh()
                time.sleep(5)
                continue
            if field is not None:
                self._fill_field(field, title)
                logging.info("Filled title: %s", title)
            else:
                logging.info(
                    "Поля названия в форме нет — сохраняю с дефолтным"
                )
            self._save_form(field, title)
            logging.info("Created event: %s", title)
            return
        self.log_page_state()
        raise AssertionError("Форму создания события открыть не удалось")

    def _open_creation_tab(self) -> bool:
        """Переключает форму на вкладку «Личное событие».

        Возвращает True, если вкладка подтвердилась (есть поле или
        активная кнопка сохранения), иначе False.
        """
        for attempt in range(3):
            elements = self.driver.find_elements(
                By.XPATH,
                "//*[normalize-space(text())='Личное событие']",
            )
            if not elements:
                elements = self.driver.find_elements(
                    By.XPATH,
                    "//*[contains(normalize-space(text()), 'Личное')]",
                )
            if not elements:
                break
            target = min(elements, key=lambda e: len(e.text or ""))
            self._click_real(target)
            time.sleep(2)
            if self._wait_any_field(timeout=3) is not None:
                logging.info("Вкладка «Личное событие» открыта")
                return True
            button = self._find_save_button()
            if button is not None and button.is_enabled():
                logging.info("Вкладка открыта, поле не найдено")
                return True
            logging.info(
                "Вкладка не переключилась, повторяю (%d)", attempt + 1
            )
        logging.info("Вкладку «Личное событие» подтвердить не удалось")
        return False

    def _wait_any_field(self, timeout: int = 6) -> Optional[Any]:
        """Ждёт появление любого текстового поля, иначе None."""
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            field = self._find_text_input()
            if field is not None:
                return field
            time.sleep(1)
        return None

    def _click_free_slot(self) -> None:
        """Кликает по свободной ячейке календаря."""
        candidates = self.driver.find_elements(
            By.XPATH,
            "//*[contains(@class, 'cell') or contains(@class, 'slot') "
            "or contains(@class, 'grid-item')]",
        )
        free = [
            element
            for element in candidates
            if element.is_displayed()
            and not (element.text or "").strip()
        ]
        target = free[len(free) // 2] if free else None
        if target is None:
            self.log_page_state()
            raise AssertionError("Не найдено свободной ячейки календаря")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", target
        )
        self._click_robust(target)
        time.sleep(3)
        if not self._modal_open():
            logging.info("Одиночный клик не открыл форму — пробую двойной")
            ActionChains(self.driver).double_click(target).perform()
            time.sleep(3)
        if not self._modal_open():
            logging.info("Двойной клик не открыл форму — кликаю через JS")
            self.driver.execute_script("arguments[0].click();", target)
            time.sleep(3)
        if not self._modal_open():
            self.log_page_state()
            raise AssertionError("Форма создания не открылась")

    def _fill_modal_title(self, title: str) -> None:
        """Вводит название в первое текстовое поле открытой формы."""
        field = self._find_text_input()
        if field is None:
            self.log_page_state()
            raise AssertionError("Поле названия в форме не найдено")
        self._fill_field(field, title)
        logging.info("Filled title: %s", title)

    # --------------------- работа с полями ---------------------

    def _visible_fields(self) -> List[Any]:
        """Все видимые текстовые поля, включая contenteditable."""
        elements = self.driver.find_elements(By.XPATH, FIELD_XPATH)
        return [
            element
            for element in elements
            if element.is_displayed()
        ]

    def _is_editable(self, element: Any) -> bool:
        """True, если элемент редактируемый через isContentEditable."""
        return bool(
            self.driver.execute_script(
                "return arguments[0].isContentEditable === true;", element
            )
        )

    def _is_editable_text(self, element: Any) -> bool:
        """True для contenteditable и обычных текстовых полей."""
        if element.get_attribute("contenteditable") == "true":
            return True
        if self._is_editable(element):
            return True
        element_type: str = (
            element.get_attribute("type") or ""
        ).lower()
        return element.tag_name in ("input", "textarea") and element_type in (
            "",
            "text",
        )

    def _field_value(self, element: Any) -> str:
        """Возвращает текущее значение поля с учётом contenteditable."""
        if element.get_attribute("contenteditable") == "true":
            return element.text or ""
        if self._is_editable(element) and element.tag_name not in (
            "input",
            "textarea",
        ):
            return element.text or ""
        return element.get_attribute("value") or ""

    def _fill_field(self, element: Any, value: str) -> None:
        """Заполняет поле: реальный ввод + проверка значения."""
        element.click()
        tag: str = element.tag_name
        if tag in ("input", "textarea"):
            element.send_keys(Keys.CONTROL, "a")
        else:
            self.driver.execute_script(
                "arguments[0].focus();", element
            )
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(value)
        time.sleep(1)
        try:
            actual: str = self._field_value(element)
        except WebDriverException:
            return
        logging.info("Значение поля после ввода: '%s'", actual[:80])
        if value not in actual:
            logging.warning("Ввод не применился — задаю через JS")
            self.driver.execute_script(
                "if (arguments[0].tagName === 'INPUT' "
                "|| arguments[0].tagName === 'TEXTAREA') "
                "{ arguments[0].value = arguments[1]; } "
                "else { arguments[0].textContent = arguments[1]; }",
                element, value,
            )
            self._commit_field(element)

    def _commit_field(self, element: Any) -> None:
        """Доводит значение до Angular-модели: события + blur."""
        self.driver.execute_script(
            "arguments[0].dispatchEvent("
            "new Event('input', {bubbles: true}));"
            "arguments[0].dispatchEvent("
            "new Event('change', {bubbles: true}));"
            "arguments[0].blur();",
            element,
        )

    def _find_text_input(self) -> Optional[Any]:
        """Первое видимое текстовое поле; сначала внутри оверлея."""
        fields = self._visible_fields()
        editable_fields = [
            field
            for field in fields
            if self._is_editable_text(field)
        ]
        if not editable_fields:
            return None
        dialogs = self.driver.find_elements(
            By.XPATH, "//*[@role='dialog']"
        )
        if dialogs:
            for field in editable_fields:
                if any(
                    d for d in dialogs if self._contains(d, field)
                ):
                    return field
        return editable_fields[0]

    def _contains(self, parent: Any, child: Any) -> bool:
        """Проверяет вложенность элементов через JavaScript."""
        return self.driver.execute_script(
            "return arguments[0].contains(arguments[1]);", parent, child
        )

    def _wait_modal_closed(self, timeout: int = 10) -> None:
        """Ждёт, пока оверлей закроется (используется при создании)."""
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            if not self._modal_open():
                return
            time.sleep(1)
        logging.info("Форма всё ещё открыта после сохранения")

    # ------------------- просмотр и правка -------------------

    def open_event_details(self, title: str) -> None:
        """Открывает карточку события по названию.

        Если события нет в видимой неделе, листает календарь вперёд.
        Если поиск долго не даёт результата — обновляет страницу:
        после долгого прогона рендер календаря может запаздывать.
        """
        next_locators: List[Locator] = [
            (By.XPATH, "//button[contains(@aria-label, 'След')]"
             "[contains(@aria-label, 'еделя')]"),
            (By.XPATH, "//button[contains(@aria-label, 'Next')]"),
            (By.XPATH,
             "//*[contains(@class, 'next') or contains(@class, 'arrow')]"
             "[self::button or self::div or self::span]"),
        ]
        end = time.monotonic() + 60
        last_refresh: float = time.monotonic()
        last_error: Optional[Exception] = None
        while time.monotonic() < end:
            try:
                elements = self.driver.find_elements(
                    By.XPATH,
                    f"//*[contains(normalize-space(text()), '{title}')]",
                )
                if elements:
                    target = min(
                        elements, key=lambda e: len(e.text or "")
                    )
                    self._click_robust(target)
                    time.sleep(3)
                    logging.info("Opened event details: %s", title)
                    return
            except Exception as error:  # noqa: BLE001
                last_error = error
            try:
                self._click_first_available(
                    next_locators, "стрелка следующей недели"
                )
                time.sleep(3)
                logging.info(
                    "Событие не в видимой неделе — листаю вперёд"
                )
            except AssertionError:
                pass
            if time.monotonic() - last_refresh > 12:
                logging.info(
                    "Событие не найдено — обновляю страницу и ищу заново"
                )
                self.driver.refresh()
                time.sleep(6)
                last_refresh = time.monotonic()
            time.sleep(1)
        self.log_page_state()
        raise AssertionError(
            f"Событие '{title}' не найдено на странице"
        ) from last_error

    def _edit_mode_active(self, old_title: str) -> bool:
        """True, если на странице уже есть редактируемое поле с названием."""
        for field in self._visible_fields():
            if not self._is_editable_text(field):
                continue
            if old_title in self._field_value(field):
                return True
        return False

    def edit_event_title(self, old_title: str, new_title: str) -> None:
        """Меняет название события через интерфейс."""
        self.open_event_details(old_title)
        if not self._edit_mode_active(old_title):
            try:
                self._click_first_available(
                    self.EDIT_BUTTONS, "кнопка правки"
                )
            except AssertionError:
                logging.info(
                    "Кнопки правки нет — считаю форму уже открытой"
                )
        field = self._wait_title_input(old_title)
        self._fill_field(field, new_title)
        logging.info("Typed new title: %s", new_title)
        self._save_form(field, new_title)
        logging.info("Saved edited title: %s", new_title)

    def _wait_title_input(
        self, old_title: str, timeout: int = 10
    ) -> Any:
        """Ищет редактируемое поле, в котором сейчас старое название."""
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            for field in self._visible_fields():
                if not self._is_editable_text(field):
                    continue
                if old_title in self._field_value(field):
                    return field
            time.sleep(1)
        self.log_page_state()
        raise AssertionError(f"Поле с названием '{old_title}' не найдено")

    # ---------------------- удаление ----------------------

    def delete_event(self, title: str) -> None:
        """Удаляет событие через интерфейс с подтверждением."""
        self.open_event_details(title)
        try:
            self._click_first_available(
                self.DELETE_BUTTONS, "кнопка удаления"
            )
        except AssertionError:
            logging.info(
                "Кнопки удаления нет — открываю меню «ещё»"
            )
            self._click_first_available(
                self.MORE_BUTTONS, "меню дополнительных действий"
            )
            time.sleep(2)
            self._click_first_available(
                self.DELETE_BUTTONS, "кнопка удаления"
            )
        try:
            self._click_first_available(
                self.CONFIRM_DELETE_BUTTONS, "подтверждение удаления"
            )
        except AssertionError:
            logging.info("Подтверждение не потребовалось")
        time.sleep(3)
        logging.info("Confirmed deletion: %s", title)
