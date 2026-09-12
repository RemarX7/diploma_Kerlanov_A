import allure
import pytest
from datetime import datetime, timedelta


@allure.feature("API")
@allure.story("Расписание")
@pytest.mark.api
class TestScheduleAPI:
    """Тесты для API расписания."""

    @allure.title("Создание личного события")
    @allure.description("Проверка успешного создания личного события")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_personal_event(self, api) -> None:
        """Тест создания личного события."""
        start_at = (datetime.now() + timedelta(days=7)).replace(
            hour=19, minute=0, second=0, microsecond=0
        ).isoformat() + "+03:00"

        end_at = (datetime.now() + timedelta(days=7)).replace(
            hour=19, minute=30, second=0, microsecond=0
        ).isoformat() + "+03:00"

        with allure.step("Отправить запрос на создание события"):
            response = api.create_personal_event(
                title="Тестовое событие",
                start_at=start_at,
                end_at=end_at
            )

        with allure.step("Проверить статус ответа 200"):
            assert response.status_code == 200, f"Ошибка: {response.text}"

        with allure.step("Проверить, что событие создано"):
            data = response.json()
            assert "data" in data
            assert "payload" in data["data"]

        event_id = data["data"]["payload"]["id"]
        start_at_from_response = data["data"]["startAt"]

        with allure.step("Удалить созданное событие (постусловие)"):
            delete_response = api.delete_personal_event(event_id, start_at_from_response)
            assert delete_response.status_code == 200

    @allure.title("Обновление личного события")
    @allure.description("Проверка успешного обновления личного события")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_personal_event(self, api) -> None:
        """Тест обновления личного события."""
        start_at = (datetime.now() + timedelta(days=7)).replace(
            hour=19, minute=0, second=0, microsecond=0
        ).isoformat() + "+03:00"

        end_at = (datetime.now() + timedelta(days=7)).replace(
            hour=19, minute=30, second=0, microsecond=0
        ).isoformat() + "+03:00"

        with allure.step("Создать событие для обновления"):
            create_response = api.create_personal_event(
                title="Событие для обновления",
                start_at=start_at,
                end_at=end_at
            )
            assert create_response.status_code == 200
            data = create_response.json()
            event_id = data["data"]["payload"]["id"]
            old_start_at = data["data"]["startAt"]

        new_start_at = (datetime.now() + timedelta(days=8)).replace(
            hour=20, minute=0, second=0, microsecond=0
        ).isoformat() + "+03:00"

        new_end_at = (datetime.now() + timedelta(days=8)).replace(
            hour=20, minute=30, second=0, microsecond=0
        ).isoformat() + "+03:00"

        with allure.step("Отправить запрос на обновление события"):
            update_response = api.update_personal_event(
                event_id=event_id,
                old_start_at=old_start_at,
                new_start_at=new_start_at,
                new_end_at=new_end_at,
                title="Обновленное событие",
                description="Новое описание"
            )

        with allure.step("Проверить статус ответа 200"):
            assert update_response.status_code == 200, f"Ошибка: {update_response.text}"

        with allure.step("Удалить созданное событие"):
            delete_response = api.delete_personal_event(event_id, new_start_at)
            assert delete_response.status_code == 200

    @allure.title("Удаление личного события")
    @allure.description("Проверка успешного удаления личного события")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_personal_event(self, api) -> None:
        """Тест удаления личного события."""
        start_at = (datetime.now() + timedelta(days=7)).replace(
            hour=19, minute=0, second=0, microsecond=0
        ).isoformat() + "+03:00"

        end_at = (datetime.now() + timedelta(days=7)).replace(
            hour=19, minute=30, second=0, microsecond=0
        ).isoformat() + "+03:00"

        with allure.step("Создать событие для удаления"):
            create_response = api.create_personal_event(
                title="Событие для удаления",
                start_at=start_at,
                end_at=end_at
            )
            assert create_response.status_code == 200
            data = create_response.json()
            event_id = data["data"]["payload"]["id"]
            start_at_from_response = data["data"]["startAt"]

        with allure.step("Отправить запрос на удаление события"):
            delete_response = api.delete_personal_event(event_id, start_at_from_response)

        with allure.step("Проверить статус ответа 200"):
            assert delete_response.status_code == 200, f"Ошибка: {delete_response.text}"

    @allure.title("Создание события с невалидным токеном")
    @allure.description("Проверка ошибки авторизации при невалидном токене")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_event_invalid_token(self) -> None:
        """Тест создания события с невалидным токеном (ожидается 401)."""
        import requests
        from config.settings import BASE_URL

        url = f"{BASE_URL}/v2/schedule/createPersonal"
        headers = {
            "Cookie": "token_global=invalid_token_12345",
            "Content-Type": "application/json"
        }
        payload = {
            "backgroundColor": "#FFF7C7",
            "color": "#FAC641",
            "description": "Описание",
            "title": "Название",
            "startAt": "2028-02-29T19:00:00+03:00",
            "endAt": "2028-02-29T19:30:00+03:00"
        }

        with allure.step("Отправить запрос с невалидным токеном"):
            response = requests.post(url, headers=headers, json=payload, verify=False)

        with allure.step("Проверить статус ответа 401"):
            assert response.status_code == 401, f"Ожидался 401, получен {response.status_code}"

    @allure.title("Создание события с максимальным количеством символов в названии")
    @allure.description("Проверка валидации названия события (40 символов)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_event_max_title_length(self, api) -> None:
        """Тест создания события с названием из 40 символов."""
        start_at = (datetime.now() + timedelta(days=7)).replace(
            hour=19, minute=0, second=0, microsecond=0
        ).isoformat() + "+03:00"

        end_at = (datetime.now() + timedelta(days=7)).replace(
            hour=19, minute=30, second=0, microsecond=0
        ).isoformat() + "+03:00"

        title_40 = "A" * 40

        with allure.step("Создать событие с названием из 40 символов"):
            response = api.create_personal_event(
                title=title_40,
                start_at=start_at,
                end_at=end_at
            )

        with allure.step("Проверить, что событие создалось"):
            assert response.status_code == 200, f"Ошибка: {response.text}"
            data = response.json()
            assert "data" in data
            assert "payload" in data["data"]

        event_id = data["data"]["payload"]["id"]
        start_at_from_response = data["data"]["startAt"]

        with allure.step("Удалить созданное событие"):
            delete_response = api.delete_personal_event(event_id, start_at_from_response)
            assert delete_response.status_code == 200
