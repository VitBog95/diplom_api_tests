import requests
import allure
from config import BASE_URL


@allure.title("Негативный тест: Создание урока без токена")
def test_create_lesson_without_token():
    """Создание урока без заголовка Cookie"""

    payload = {
        "backgroundColor": "#FFF7C7",
        "color": "#FAC641",
        "title": "Урок без токена",
        "startAt": "2026-09-10T10:00:00+03:00",
        "endAt": "2026-09-10T11:00:00+03:00",
    }

    response = requests.post(f"{BASE_URL}/v2/schedule/createPersonal", json=payload)

    assert response.status_code == 401
    json_data = response.json()
    assert json_data.get("code") == 401
    assert "Authentication required" in json_data.get("message", "")

    print("✅ Негативный тест пройден: 401 Unauthorized")
