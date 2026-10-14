# Skyeng Teachers Autotests

UI- и API-автотесты кабинета учителя Skyeng (new-teachers.skyeng.ru).
Стек: Python, pytest, Selenium (UI), Requests (API), Allure, Page Object.

## Установка
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env         # заполните LOGIN, PASSWORD, TOKEN_GLOBAL

## Запуск
pytest -m "ui" --alluredir=allure-results     # только UI-тесты
pytest -m "api" --alluredir=allure-results    # только API-тесты
pytest --alluredir=allure-results             # все тесты
allure serve allure-results                   # просмотр отчёта

Ссылка на итоговую страницу работы: <ссылка на Yonote>