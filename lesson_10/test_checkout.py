import pytest
import allure
from allure import severity, severity_level

# ✅ ВАЖНО: полные импорты через lesson_10
from lesson_10.login_page import LoginPage
from lesson_10.inventory_page import InventoryPage
from lesson_10.cart_page import CartPage
from lesson_10.checkout_page import CheckoutPage


@allure.title("Оформление заказа: полный сценарий")
@allure.description("Логин → добавление товара → корзина → оформление → проверка суммы")
@allure.feature("Оформление заказа")
@severity(severity_level.CRITICAL)
def test_checkout_flow(driver):
    # 1. Логин (теперь точно сработает)
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    # Проверка, что попали на страницу каталога
    assert "inventory.html" in driver.current_url, f"Ожидался inventory.html, а открыт: {driver.current_url}"

    inventory = InventoryPage(driver)

    # 2. Ждём, пока появятся карточки товаров (это важно, чтобы не искать кнопку раньше времени)
    inventory.wait_for_page_loaded()

    cart = CartPage(driver)
    checkout = CheckoutPage(driver)

    with allure.step("Добавить рюкзак в корзину"):
        inventory.add_backpack_to_cart()

    with allure.step("Перейти в корзину"):
        inventory.go_to_cart()

    with allure.step("Продолжить оформление"):
        cart.proceed_to_checkout()

    with allure.step("Заполнить данные покупателя"):
        checkout.fill_personal_info("John", "Doe", "12345")

    with allure.step("Продолжить к финальному экрану"):
        checkout.continue_checkout()

    total = checkout.get_total_amount()
    assert total > 0, f"Сумма заказа должна быть больше 0, получено: {total}"