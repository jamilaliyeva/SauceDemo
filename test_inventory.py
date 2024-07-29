import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import test_login


class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.add_button = (By.ID, "add-to-cart-sauce-labs-backpack")
        self.count_button = (By.CLASS_NAME, "shopping_cart_badge")
        self.inventory_button = (By.CLASS_NAME, "shopping_cart_link")
        self.wait = WebDriverWait(driver, 10)

    def add_item_to_cart(self, item):
        self.driver.find_element(*self.add_button).click()

    def inventory_button(self, item):
        self.driver.find_element(*self.inventory_button).click()

    def get_count(self, item):
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.count_button))
            return int(element.text)
        except:
            return 0

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_successful_login(driver):
    login = test_login.LoginPage(driver)
    login.load()
    login.set_username('standard_user')
    login.set_password('secret_sauce')
    login.click_login()

    assert "https://www.saucedemo.com/inventory.html" in driver.current_url


def adding_item_to_cart(driver):
    login = test_login.LoginPage(driver)
    login.load()
    login.set_username('standard_user')
    login.set_password('secret_sauce')
    login.click_login()

    inventory = InventoryPage(driver)
    inventory.add_item_to_cart()

    assert 1 == inventory.get_count()
