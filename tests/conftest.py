# tests/conftest.py
import pytest
import requests
from config import BASE_URL, MY_TOKEN

@pytest.fixture
def auth_headers():
    """Заголовки для авторизованных запросов"""
    return {
        "Cookie": f"token_global={MY_TOKEN}",
        "Content-Type": "application/json"
    }

@pytest.fixture
def created_lesson(auth_headers):
    """Создает урок и возвращает его id и startAt"""
    
    payload = {
        "backgroundColor": "#FFF7C7",
        "color": "#FAC641",
        "title": "Урок для теста",
        "startAt": "2026-09-10T10:00:00+03:00",
        "endAt": "2026-09-10T11:00:00+03:00"
    }
    
    response = requests.post(
        f"{BASE_URL}/v2/schedule/createPersonal",
        headers=auth_headers,
        json=payload
    )
    
    assert response.status_code == 200
    json_data = response.json()
    assert json_data.get("errors") is None
    assert "id" in json_data["data"]["payload"]
    
    lesson_id = json_data["data"]["payload"]["id"]
    start_at = json_data["data"]["startAt"]
    
    return {"id": lesson_id, "startAt": start_at}