"""UI тесты для расписания Skyeng."""

import allure
import pytest
from pages.login_page import LoginPage
from datetime import datetime, timedelta
from pages.schedule_page import SchedulePage
from config.settings import LOGIN, PASSWORD, UI_LOGIN_URL


@allure.feature("UI")
@allure.story("Расписание")
@pytest.mark.ui
class TestScheduleUI:
    """UI тесты для расписания."""

    @allure.title("Создание личного события")
    @allure.description("Проверка создания личного события через UI")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_personal_event(self, driver) -> None:
        """Тест создания личного события через UI."""
        event_title = f"Автотест {datetime.now().strftime('%H%M%S')}"

        with allure.step("Авторизоваться на сайте"):
            login_page = LoginPage(driver)
            login_page.open_login_page(UI_LOGIN_URL)
            login_page.login(LOGIN, PASSWORD)

        with allure.step("Перейти в расписание и закрыть поп-ап"):
            schedule_page = SchedulePage(driver)
            schedule_page.close_popup_if_exists()
            schedule_page.go_to_schedule()

        with allure.step("Открыть модалку создания события"):
            schedule_page.click_create_button()
            schedule_page.select_personal_event()

        with allure.step("Заполнить название события"):
            schedule_page.input_title(event_title)

        with allure.step("Выбрать дату и время"):
            schedule_page.select_start_date(1)
            schedule_page.input_start_time("19:00")
            schedule_page.input_end_time("19:30")

        with allure.step("Нажать 'Сохранить'"):
            schedule_page.click_save()

        with allure.step("Проверить, что событие появилось в календаре"):
            assert schedule_page.is_event_in_calendar(event_title), \
                f"Событие '{event_title}' не найдено в календаре"

    @allure.title("Создание события с максимальным названием (40 символов)")
    @allure.description("Проверка валидации названия события")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_event_max_title(self, driver) -> None:
        """Тест создания события с названием из 40 символов."""
        event_title = "A" * 40

        with allure.step("Авторизоваться"):
            login_page = LoginPage(driver)
            login_page.open_login_page(UI_LOGIN_URL)
            login_page.login(LOGIN, PASSWORD)

        with allure.step("Перейти в расписание"):
            schedule_page = SchedulePage(driver)
            schedule_page.close_popup_if_exists()
            schedule_page.go_to_schedule()

        with allure.step("Открыть модалку и выбрать 'Личное событие'"):
            schedule_page.click_create_button()
            schedule_page.select_personal_event()

        with allure.step("Ввести название из 40 символов"):
            schedule_page.input_title(event_title)

        with allure.step("Проверить, что название введено (40 символов)"):
            title_value = schedule_page.find_element(
                SchedulePage.TITLE_INPUT
            ).get_attribute("value")
            assert len(title_value) == 40, \
                f"Ожидалось 40 символов, получено {len(title_value)}"

        with allure.step("Выбрать дату и время"):
            schedule_page.select_start_date(1)
            schedule_page.input_start_time("20:00")
            schedule_page.input_end_time("20:30")

        with allure.step("Нажать 'Сохранить'"):
            schedule_page.click_save()

        with allure.step("Проверить, что событие появилось в календаре"):
            assert schedule_page.is_event_in_calendar(event_title), \
                "Событие с 40-символьным названием не найдено"

    @allure.title("Создание события разных цветов")
    @allure.description("Проверка выбора цвета личного события")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_event_with_color(self, driver) -> None:
        """Тест создания события с выбранным цветом."""
        event_title = f"Цветное {datetime.now().strftime('%H%M%S')}"
        # Индекс 3 — фиолетовый цвет (последний в списке)
        color_index = 3
        expected_bg_color = "rgb(249, 235, 255)"  # фиолетовый

        with allure.step("Авторизоваться"):
            login_page = LoginPage(driver)
            login_page.open_login_page(UI_LOGIN_URL)
            login_page.login(LOGIN, PASSWORD)

        with allure.step("Перейти в расписание"):
            schedule_page = SchedulePage(driver)
            schedule_page.close_popup_if_exists()
            schedule_page.go_to_schedule()

        with allure.step("Открыть модалку и выбрать 'Личное событие'"):
            schedule_page.click_create_button()
            schedule_page.select_personal_event()

        with allure.step("Заполнить название"):
            schedule_page.input_title(event_title)

        with allure.step("Выбрать дату и время"):
            schedule_page.select_start_date(1)
            schedule_page.input_start_time("21:00")
            schedule_page.input_end_time("21:30")

        with allure.step(f"Выбрать цвет (индекс {color_index})"):
            schedule_page.select_color(color_index)

        with allure.step("Нажать 'Сохранить'"):
            schedule_page.click_save()

        with allure.step("Проверить цвет события"):
            style = schedule_page.get_event_background_color(event_title)
            assert expected_bg_color in style, \
                f"Ожидался цвет {expected_bg_color}, получен style: {style}"

    @allure.title("Создание события с минимальной длительностью (5 минут)")
    @allure.description("Проверка создания события длительностью 5 минут")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_event_min_duration(self, driver, api) -> None:
        """Тест создания события длительностью 5 минут."""
        event_title = "Короткое событие"
        start_time_str = "19:00"
        end_time_str = "19:05"
        expected_duration = 5

        with allure.step("Авторизоваться"):
            login_page = LoginPage(driver)
            login_page.open_login_page(UI_LOGIN_URL)
            login_page.login(LOGIN, PASSWORD)

        with allure.step("Передать токен из браузера в API клиент"):
            for cookie in driver.get_cookies():
                if cookie["name"] == "token_global":
                    api.set_token(f"token_global={cookie['value']}")
                    break

        with allure.step("Перейти в расписание"):
            schedule_page = SchedulePage(driver)
            schedule_page.close_popup_if_exists()
            schedule_page.go_to_schedule()

        with allure.step("Открыть модалку и выбрать 'Личное событие'"):
            schedule_page.click_create_button()
            schedule_page.select_personal_event()

        with allure.step("Установить дату и время"):
            schedule_page.select_start_date(1)
            schedule_page.input_start_time(start_time_str)
            schedule_page.input_end_time(end_time_str)

        with allure.step("Заполнить название события"):
            schedule_page.input_title(event_title)

        with allure.step("Нажать 'Сохранить'"):
            schedule_page.click_save()

        with allure.step("Проверить через API, что событие создано с длительностью 5 минут"):
            from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S+03:00")
            till_date = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%dT%H:%M:%S+03:00")

            response = api.get_events(from_date, till_date)
            assert response.status_code == 200, f"Ошибка API: {response.text}"

            events = response.json()["data"]["events"]

            # Ищем наше событие по названию (title на 2 уровня глубже!)
            our_event = next(
                (
                    e for e in events
                    if e.get("payload", {}).get("payload", {}).get("title")
                    == event_title
                ),
                None
            )
            assert our_event is not None, f"Событие '{event_title}' не найдено"

            # Проверяем длительность
            duration_seconds = our_event.get("durationSeconds")
            actual_duration_minutes = duration_seconds / 60

            assert actual_duration_minutes == expected_duration, \
                f"Ожидалось {expected_duration} мин, получено {actual_duration_minutes} мин"

    @allure.title("Проверка неактивности кнопки 'Сохранить' без названия")
    @allure.description("Проверка валидации обязательного поля 'Название'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_save_button_disabled_without_title(self, driver) -> None:
        """Тест проверки неактивности кнопки без названия."""
        with allure.step("Авторизоваться"):
            login_page = LoginPage(driver)
            login_page.open_login_page(UI_LOGIN_URL)
            login_page.login(LOGIN, PASSWORD)

        with allure.step("Перейти в расписание"):
            schedule_page = SchedulePage(driver)
            schedule_page.close_popup_if_exists()
            schedule_page.go_to_schedule()

        with allure.step("Открыть модалку и выбрать 'Личное событие'"):
            schedule_page.click_create_button()
            schedule_page.select_personal_event()

        with allure.step("Проверить, что кнопка 'Сохранить' неактивна без названия"):
            assert not schedule_page.is_save_button_enabled(), \
                "Кнопка 'Сохранить' должна быть неактивна без названия"
