from telnetlib import EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    def __init__(self, driver):
        self.url = "https://www.saucedemo.com/"
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.driver.implicitly_wait(10)
        self.user = (By.ID, 'user-name')
        self.passwd = (By.ID, 'password')
        self.login_button = (By.ID, 'login-button')
        self.error_message = (By.CLASS_NAME, "error-message-container")

    def load(self):
        self.driver.get(self.url)

    def set_username(self, username):
        self.driver.find_element(*self.user).send_keys(username)

    def set_password(self, password):
        self.driver.find_element(*self.passwd).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()

    def get_error_message(self):
        return self.driver.find_element(*self.error_message).text


def successful_login():
    driver = webdriver.Chrome()
    login = LoginPage(driver)
    login.load()
    login.set_username('standard_user')
    login.set_password('secret_sauce')
    login.click_login()

    # Ждем, пока элемент на странице инвентаря станет видимым
    login.wait.until(EC.url_contains("inventory.html"))

    assert "https://www.saucedemo.com/inventory.html" in driver.current_url

    driver.quit()


def failed_login_with_wrong_credentials():
    driver = webdriver.Chrome()
    login = LoginPage(driver)
    login.load()
    login.set_username('just_user')
    login.set_password('12345')
    login.click_login()

    # Ждем появления сообщения об ошибке
    login.wait.until(EC.visibility_of_element_located(login.error_message))

    assert "Epic sadface: Username and password do not match any user in this service" in login.get_error_message()

    driver.quit()


def failed_login_with_blank_credentials():
    driver = webdriver.Chrome()
    login = LoginPage(driver)
    login.load()
    login.click_login()

    # Ждем появления сообщения об ошибке
    login.wait.until(EC.visibility_of_element_located(login.error_message))

    assert "Epic sadface: Username is required" in login.get_error_message()

    driver.quit()


successful_login()
failed_login_with_wrong_credentials()
failed_login_with_blank_credentials()
