"""Страница авторизации Skyeng."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Страница авторизации Skyeng."""

    # Локаторы
    PASSWORD_AUTH_LINK = (By.CSS_SELECTOR, ".js-send-otp-form-to-username-password")
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    SUBMIT_BUTTON = (
        By.XPATH,
        "//button[.//span[contains(@class, 'js-username-password-form-button')]]"
    )

    def __init__(self, driver: WebDriver) -> None:
        """Инициализация страницы авторизации."""
        super().__init__(driver)

    @allure.step("Открыть страницу авторизации")
    def open_login_page(self, url: str) -> None:
        """Открыть страницу авторизации."""
        self.driver.get(url)

    @allure.step("Нажать 'Войти с помощью пароля'")
    def click_password_auth_link(self) -> None:
        """Нажать ссылку 'Войти с помощью пароля'."""
        self.click(self.PASSWORD_AUTH_LINK)

    @allure.step("Ввести логин")
    def input_username(self, username: str) -> None:
        """Ввести логин."""
        self.send_keys(self.USERNAME_INPUT, username)

    @allure.step("Ввести пароль")
    def input_password(self, password: str) -> None:
        """Ввести пароль."""
        self.send_keys(self.PASSWORD_INPUT, password)

    @allure.step("Нажать 'Войти'")
    def click_submit(self) -> None:
        """Нажать кнопку 'Войти'."""
        self.click(self.SUBMIT_BUTTON)

    @allure.step("Выполнить полный вход в систему")
    def login(self, username: str, password: str) -> None:
        """Полный сценарий авторизации."""
        self.click_password_auth_link()
        self.input_username(username)
        self.input_password(password)
        self.click_submit()
