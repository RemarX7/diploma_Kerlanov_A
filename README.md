# Дипломная работа: Автоматизация UI- и API-тестов

## Описание проекта

Проект содержит автоматизированные тесты для веб-приложения Skyeng (вкладка "Расписание"). Реализованы UI- и API-тесты с использованием паттерна Page Object, фреймворка pytest и генерации отчётов Allure.

## Ссылка на финальный проект по ручному тестированию

[Финальная работа по ручному тестированию](https://github.com/RemarX7/diploma_Kerlanov_A)

## Структура проекта

diploma_Kerlanov_A/
├── api/                       # API клиенты
│   └── schedule_api.py        # API клиент для работы с расписанием
├── config/                    # Конфигурация
│   └── settings.py            # Настройки (URL, логин, пароль)
├── pages/                     # Page Object классы
│   ├── base_page.py           # Базовый класс страницы
│   ├── login_page.py          # Страница авторизации
│   └── schedule_page.py       # Страница расписания
├── test/                      # Тесты
│   ├── test_api.py            # API-тесты
│   └── test_ui.py             # UI-тесты
├── .env                       # Переменные окружения (не пушится в git)
├── .flake8                    # Настройки линтера
├── .gitignore                 # Игнорируемые файлы
├── conftest.py                # Фикстуры и маркеры pytest
├── README.md                  # Документация
└── requirements.txt           # Зависимости

## Требования

- Python 3.12+
- Google Chrome (последняя версия)
- ChromeDriver (совместимый с версией Chrome)

## Установка

### 1. Клонирование репозитория

git clone https://github.com/RemarX7/diploma_Kerlanov_A.git
cd diploma_Kerlanov_A

### 2. Создание виртуального окружения

python -m venv venv
venv\Scripts\activate

### 3. Установка зависимостей

pip install -r requirements.txt

### 4. Создание .env файла

Создайте файл `.env` в корне проекта:

BASE_URL=https://api-teachers.skyeng.ru
UI_BASE_URL=https://skyeng.ru
UI_LOGIN_URL=https://id.skyeng.ru/login
UI_SCHEDULE_URL=https://teacher.skyeng.ru/schedule
TOKEN=token_global=ваш_токен
LOGIN=ваш_логин
PASSWORD=ваш_пароль

Важно: токен можно получить в DevTools браузера после авторизации (Application → Cookies → token_global).

## Запуск тестов

### Все тесты

pytest

### Только UI-тесты

pytest -m ui

### Только API-тесты

pytest -m api

### Конкретный тест

pytest test/test_ui.py::TestScheduleUI::test_create_personal_event

### С генерацией Allure-отчёта

pytest --alluredir=allure-results
allure serve allure-results

## Формирование Allure-отчёта

### 1. Запуск тестов с сохранением результатов

pytest --alluredir=allure-results

### 2. Просмотр отчёта (быстрый способ)

allure serve allure-results

Команда запустит локальный сервер и откроет отчёт в браузере.

### 3. Или генерация HTML-отчёта

allure generate allure-results -o allure-report --clean
allure open allure-report

## Проверка стиля кода (PEP8)

flake8 .

## Реализованные тесты

### API-тесты (5)

1. test_create_personal_event — Создание личного события
2. test_update_personal_event — Обновление события
3. test_delete_personal_event — Удаление события
4. test_create_event_invalid_token — Ошибка 401 при невалидном токене
5. test_create_event_max_title_length — Валидация названия (40 символов)

### UI-тесты (5)

1. test_create_personal_event — Создание события через UI
2. test_create_event_max_title — 40-символьное название
3. test_create_event_with_color — Выбор цвета события
4. test_create_event_min_duration — Длительность события (через API)
5. test_save_button_disabled_without_title — Кнопка неактивна без названия

## Технологии

- Python 3.12
- pytest — фреймворк для тестирования
- selenium — автоматизация браузера
- requests — HTTP-запросы для API-тестов
- allure-pytest — генерация отчётов
- python-dotenv — переменные окружения
- flake8 — проверка стиля кода

## Автор

Александр Керланов (@RemarX7)
