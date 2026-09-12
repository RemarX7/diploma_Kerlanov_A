"""Настройки проекта."""

import os
from dotenv import load_dotenv

load_dotenv()

# URL API
BASE_URL = os.getenv("BASE_URL")

# URL UI
UI_BASE_URL = os.getenv("UI_BASE_URL", "https://skyeng.ru")
UI_LOGIN_URL = os.getenv("UI_LOGIN_URL", "https://id.skyeng.ru/login")
UI_SCHEDULE_URL = os.getenv("UI_SCHEDULE_URL", "https://teacher.skyeng.ru/schedule")

# Данные для авторизации
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
TOKEN = os.getenv("TOKEN")

if not BASE_URL:
    raise ValueError("BASE_URL не найден в .env файле!")
