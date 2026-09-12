"""Страница расписания Skyeng."""

import allure
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage


class SchedulePage(BasePage):
    """Страница расписания Skyeng."""

    # Левое меню
    SCHEDULE_MENU = (By.CSS_SELECTOR, "[data-qa-id='left-menu-item:Расписание']")

    # Поп-ап
    POPUP_CLOSE = (By.CSS_SELECTOR, ".cbw-popup-close-top")

    # Кнопка "Создать"
    CREATE_BUTTON = (
        By.XPATH,
        "//button[.//div[contains(@class, 'content') and contains(text(), 'Создать')]]"
    )

    # Радиобаттоны
    PERSONAL_EVENT_RADIO = (
        By.XPATH,
        "//label[.//span[contains(text(), 'Личное событие')]]"
    )

    # Поля формы
    TITLE_INPUT = (By.CSS_SELECTOR, "input[placeholder='Например: посмотреть вебинар']")
    DESCRIPTION_INPUT = (By.CSS_SELECTOR, "textarea[placeholder='Например: ссылка на вебинар']")
    DATE_SELECTS = (By.CSS_SELECTOR, "select.-size-s.-state-default.-type-default.select")
    TIME_INPUTS = (By.CSS_SELECTOR, "input.input__centered")
    REPEAT_SELECT = (By.CSS_SELECTOR, "ds-select.select select")

    # Цвета
    COLOR_CIRCLES = (By.CSS_SELECTOR, ".color-circle")

    # Кнопка "Сохранить"
    SAVE_BUTTON = (
        By.XPATH,
        "//button[.//div[contains(@class, 'content') and contains(text(), 'Сохранить')]]"
    )

    def __init__(self, driver: WebDriver) -> None:
        """Инициализация страницы расписания."""
        super().__init__(driver)

    @allure.step("Перейти в расписание")
    def go_to_schedule(self) -> None:
        """Перейти в раздел 'Расписание'."""
        self.click(self.SCHEDULE_MENU)

    @allure.step("Закрыть поп-ап")
    def close_popup_if_exists(self) -> None:
        """Закрыть поп-ап если он есть."""
        try:
            self.click(self.POPUP_CLOSE)
        except Exception:
            pass

    @allure.step("Нажать кнопку 'Создать'")
    def click_create_button(self) -> None:
        """Нажать кнопку 'Создать'."""
        self.click(self.CREATE_BUTTON)

    @allure.step("Выбрать 'Личное событие'")
    def select_personal_event(self) -> None:
        """Переключиться на категорию 'Личное событие'."""
        self.click(self.PERSONAL_EVENT_RADIO)

    @allure.step("Ввести название события")
    def input_title(self, title: str) -> None:
        """Ввести название события."""
        self.send_keys(self.TITLE_INPUT, title)

    @allure.step("Ввести описание события")
    def input_description(self, description: str) -> None:
        """Ввести описание события."""
        self.send_keys(self.DESCRIPTION_INPUT, description)

    @allure.step("Выбрать дату начала")
    def select_start_date(self, date_index: int = 1) -> None:
        """Выбрать дату начала из выпадающего списка."""
        selects = self.find_elements(self.DATE_SELECTS)
        if selects:
            selects[0].click()
            options = selects[0].find_elements(By.TAG_NAME, "option")
            if len(options) > date_index:
                options[date_index].click()

    @allure.step("Ввести время начала: {time}")
    def input_start_time(self, time: str) -> None:
        """Ввести время начала."""
        inputs = self.find_elements(self.TIME_INPUTS)
        if inputs:
            inputs[0].click()
            inputs[0].send_keys(Keys.CONTROL, "a")
            inputs[0].send_keys(Keys.BACKSPACE)
            inputs[0].send_keys(time)

    @allure.step("Ввести время окончания: {time}")
    def input_end_time(self, time: str) -> None:
        """Ввести время окончания."""
        inputs = self.find_elements(self.TIME_INPUTS)
        if len(inputs) > 1:
            self.driver.execute_script("arguments[0].click();", inputs[1])
            inputs[1].send_keys(Keys.CONTROL, "a")
            inputs[1].send_keys(Keys.BACKSPACE)
            inputs[1].send_keys(time)

    @allure.step("Выбрать цвет события (индекс {index})")
    def select_color(self, index: int) -> None:
        """Выбрать цвет события по индексу (0-3)."""
        colors = self.find_elements(self.COLOR_CIRCLES)
        if index < len(colors):
            colors[index].click()

    @allure.step("Нажать 'Сохранить'")
    def click_save(self) -> None:
        """Нажать кнопку 'Сохранить'."""
        self.click(self.SAVE_BUTTON)

    def is_save_button_enabled(self) -> bool:
        """Проверить, активна ли кнопка 'Сохранить'."""
        button = self.find_element(self.SAVE_BUTTON)
        return "disabled" not in (button.get_attribute("class") or "")

    @allure.step("Найти событие в календаре по названию: {title}")
    def find_event_by_title(self, title: str) -> WebElement:
        """
        Найти событие в календаре по названию.

        Args:
            title: Название события

        Returns:
            WebElement: Найденный контейнер события
        """
        locator = (
            By.XPATH,
            f"//tcc-calendar-event-personal["
            f".//div[@class='long-view__title' and text()='{title}']"
            f"]"
        )
        return self.find_element(locator)

    @allure.step("Проверить, что событие есть в календаре: {title}")
    def is_event_in_calendar(self, title: str) -> bool:
        """
        Проверить, что событие есть в календаре.

        Args:
            title: Название события

        Returns:
            bool: True если событие найдено
        """
        locator = (
            By.XPATH,
            f"//tcc-calendar-event-personal["
            f".//div[@class='long-view__title' and text()='{title}']"
            f"]"
        )
        return self.is_element_visible(locator)

    @allure.step("Получить цвет события: {title}")
    def get_event_background_color(self, title: str) -> str:
        """
        Получить цвет фона события в календаре.

        Args:
            title: Название события

        Returns:
            str: CSS цвет фона (например, 'rgb(249, 235, 255)')
        """
        locator = (
            By.XPATH,
            f"//tcc-calendar-event-personal["
            f".//div[@class='long-view__title' and text()='{title}']"
            f"]//div[contains(@class, 'personal-container')]"
        )
        element = self.find_element(locator)
        return element.get_attribute("style")
