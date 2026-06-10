from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_dynamic_loading():
    driver = webdriver.Chrome()

    try:
        # 1. Откройте страницу https://the-internet.herokuapp.com/dynamic_loading/2
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")

        # 2. Найдите и нажмите на кнопку "Start"
        start_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[onclick='start()']"))
        )
        start_button.click()

        # 3. Дождитесь появления текста "Hello World!"
        hello_world_element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, "finish"))
        )

        # Ждём, пока текст внутри элемента станет "Hello World!"
        WebDriverWait(driver, 10).until(
            lambda d: hello_world_element.text == "Hello World!"
        )

        # 4. Сделайте скриншот страницы
        driver.save_screenshot("screenshot.png")

        # 5. Проверьте, что появившийся текст равен "Hello World!"
        assert hello_world_element.text == "Hello World!", "Текст не соответствует ожидаемому: 'Hello World!'"
        print("Тест пройден успешно: текст 'Hello World!' найден и скриншот сохранён.")

    except Exception as e:
        print(f"Тест не пройден. Ошибка: {e}")
        driver.save_screenshot("error_screenshot.png")  # Скриншот при ошибке

    finally:
        driver.quit()

