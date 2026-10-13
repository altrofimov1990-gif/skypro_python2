@allure.title("Оформление заказа: добавление товара и переход к оплате")
@severity(severity_level.CRITICAL)
def test_checkout_flow(driver):
    # 1. Авторизация — критически важно для Swag Labs
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    # 2. Проверка URL (чтобы убедиться, что нас не перекинуло)
    assert "inventory.html" in driver.current_url, f"Ожидался inventory.html, а открыт: {driver.current_url}"

    inventory = InventoryPage(driver)
    cart = CartPage(driver)
    checkout = CheckoutPage(driver)

    # 3. Перед кликом можно сделать скриншот — это спасает в отчётах Allure
    # driver.save_screenshot("before_add_to_cart.png")

    with allure.step("Добавить рюкзак в корзину"):
        inventory.add_backpack_to_cart()

    with allure.step("Перейти в корзину"):
        inventory.go_to_cart()
