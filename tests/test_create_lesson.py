import requests
import allure
from config import BASE_URL


@allure.title("Создание урока с валидными данными")
def test_create_lesson(auth_headers):
    """TC-API-01: Создание урока с валидными данными"""

    payload = {
        "backgroundColor": "#FFF7C7",
        "color": "#FAC641",
        "title": "Автотест: Урок с учеником",
        "startAt": "2026-09-10T10:00:00+03:00",
        "endAt": "2026-09-10T11:00:00+03:00",
    }

    response = requests.post(
        f"{BASE_URL}/v2/schedule/createPersonal", headers=auth_headers, json=payload
    )

    assert response.status_code == 200
    json_data = response.json()
    assert json_data.get("errors") is None
    assert "id" in json_data["data"]["payload"]

    print(f"✅ Урок создан с ID: {json_data['data']['payload']['id']}")
