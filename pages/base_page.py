from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple, List


class BasePage:
    """Базовый класс для всех страниц."""

    def __init__(self, driver: WebDriver) -> None:
        """Инициализация базовой страницы."""
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator: Tuple[str, str]) -> WebElement:
        """Найти один элемент на странице."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """Найти все элементы по локатору."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator: Tuple[str, str]) -> None:
        """Кликнуть по элементу."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def send_keys(self, locator: Tuple[str, str], text: str) -> None:
        """Ввести текст в поле."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: Tuple[str, str]) -> str:
        """Получить текст элемента."""
        return self.find_element(locator).text

    def is_element_visible(self, locator: Tuple[str, str]) -> bool:
        """Проверить видимость элемента."""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
        except Exception:
            return False
