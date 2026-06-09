from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def click_dynamic_id_button():
    # Инициализация драйвера Chrome
    driver = webdriver.Chrome()

    try:
        # Открытие страницы
        driver.get("http://uitestingplayground.com/dynamicid")

        # Ожидание загрузки страницы
        time.sleep(2)

        # Явное ожидание появления кнопки и её кликабельности
        wait = WebDriverWait(driver, 10)
        button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
        )

        # Клик по кнопке
        button.click()

        print("Кнопка успешно нажата!")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        # Закрытие браузера
        driver.quit()

if __name__ == "__main__":
    click_dynamic_id_button()