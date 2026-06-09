from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_form_test():
    # Инициализация драйвера Firefox
    driver = webdriver.Firefox()

    try:
        # Открытие страницы
        driver.get("http://the-internet.herokuapp.com/login")

        # Ожидание загрузки страницы и появления полей ввода
        wait = WebDriverWait(driver, 10)

        # Поиск и заполнение поля username
        username_field = wait.until(
            EC.element_to_be_clickable((By.ID, "username"))
        )
        username_field.send_keys("tomsmith")
        print("Введён логин: tomsmith")

        # Поиск и заполнение поля password
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("SuperSecretPassword!")
        print("Введён пароль: SuperSecretPassword!")

        # Поиск кнопки Login и клик по ней
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        print("Нажата кнопка Login")

        # Ожидание появления зелёной плашки с сообщением об успехе
        success_message = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.success"))
        )

        # Извлечение текста из плашки (удаление лишних символов, например, иконки '×')
        message_text = success_message.text.strip()
        # Удаляем последний символ (обычно это '×'), если он есть
        if message_text.endswith('×'):
            message_text = message_text[:-1].strip()

        print("Текст с зелёной плашки:")
        print(message_text)

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        # Закрытие браузера
        driver.quit()
        print("Браузер закрыт")

if __name__ == "__main__":
    login_form_test()