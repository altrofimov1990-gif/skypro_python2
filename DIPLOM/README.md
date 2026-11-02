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

## Получение TOKEN_GLOBAL

Проект не умеет логиниться по паролю: кабинет учителя использует одноразовый код,
поэтому авторизация выполняется через cookie `token_global`, которую нужно получить
вручную и положить в `.env`.

1. Откройте https://teachers.skyeng.ru и войдите в кабинет учителя.
2. Нажмите `F12` (DevTools) → вкладка **Application** (в Safari/Firefox — «Хранилище» / «Storage»).
3. Слева раскройте **Cookies** и выберите `https://teachers.skyeng.ru`.
4. Найдите строку `token_global` и скопируйте значение колонки **Value** целиком:
   в поле Value нажмите `Ctrl+A`, затем `Ctrl+C` (токен длинный, вручную легко обрезать).
5. Создайте файл `.env` в корне проекта и добавьте строку:

6. Токен периодически истекает. Если автотесты возвращают
`401 {"code":401,"message":"Authentication required"}` — перелогиньтесь
в кабинете и повторите шаги 2–5.

## Установка и запуск

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest -vv

Отчёт Allure:
allure generate allure-results -o allure-report --clean
allure open allure-report

Mac / Linux (bash, zsh)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -vv

Отчёт Allure:
allure generate allure-results -o allure-report --clean
allure open allure-report

pytest tests/test_api.py -vv      # только API-тесты
pytest tests/test_ui.py -vv       # только UI-тесты
pytest -m api -vv                 # по маркеру
