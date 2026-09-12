import os
import requests
import allure
from config.settings import BASE_URL, LOGIN, PASSWORD


class ScheduleAPI:
    """Класс для работы с API расписания."""

    def __init__(self):
        self.session = requests.Session()
        self.token = None

        # Сначала пробуем использовать токен из .env
        token_from_env = os.getenv("TOKEN")
        if token_from_env:
            self.token = token_from_env
            self.session.headers.update({
                "Cookie": self.token,
                "Content-Type": "application/json"
            })
            return

        # Если токена нет — делаем авторизацию
        self._login()

    @allure.step("Авторизация")
    def _login(self) -> None:
        """Выполнить авторизацию и сохранить токен."""
        url = f"{BASE_URL}/v2/auth/login"
        payload = {
            "email": LOGIN,
            "password": PASSWORD
        }
        response = requests.post(url, json=payload, verify=False)
        if response.status_code == 200:
            token = response.json().get("data", {}).get("token")
            if token:
                self.token = f"token_global={token}"
                self.session.headers.update({
                    "Cookie": self.token,
                    "Content-Type": "application/json"
                })
                return
        raise Exception(f"Авторизация не удалась: {response.text}")

    @allure.step("Создать личное событие")
    def create_personal_event(self, title: str, start_at: str, end_at: str,
                              color: str = "#FAC641",
                              background_color: str = "#FFF7C7",
                              description: str = "Описание события") -> dict:
        """Создание личного события."""
        url = f"{BASE_URL}/v2/schedule/createPersonal"
        payload = {
            "backgroundColor": background_color,
            "color": color,
            "description": description,
            "title": title,
            "startAt": start_at,
            "endAt": end_at
        }
        response = self.session.post(url, json=payload, verify=False)
        return response

    @allure.step("Получить расписание")
    def get_events(self, from_date: str, till_date: str) -> dict:
        """Получение событий за период."""
        url = f"{BASE_URL}/v2/schedule/events"
        payload = {
            "from": from_date,
            "till": till_date,
            "onlyTypes": []
        }
        response = self.session.post(url, json=payload, verify=False)
        return response

    @allure.step("Обновить личное событие")
    def update_personal_event(self, event_id: int, old_start_at: str,
                              new_start_at: str, new_end_at: str,
                              title: str = "Обновленное название",
                              description: str = "Обновленное описание") -> dict:
        """Обновление личного события."""
        url = f"{BASE_URL}/v2/schedule/updatePersonal"
        payload = {
            "id": event_id,
            "oldStartAt": old_start_at,
            "backgroundColor": "#FFF7C7",
            "color": "#FAC641",
            "description": description,
            "title": title,
            "startAt": new_start_at,
            "endAt": new_end_at
        }
        response = self.session.post(url, json=payload, verify=False)
        return response

    @allure.step("Удалить личное событие")
    def delete_personal_event(self, event_id: int, start_at: str) -> dict:
        """Удаление личного события."""
        url = f"{BASE_URL}/v2/schedule/removePersonal"
        payload = {
            "id": event_id,
            "startAt": start_at
        }
        response = self.session.post(url, json=payload, verify=False)
        return response

    @allure.step("Установить токен из cookies")
    def set_token(self, token: str) -> None:
        """Установить токен из cookies браузера."""
        self.token = token
        self.session.headers.update({
            "Cookie": token,
            "Content-Type": "application/json"
        })
