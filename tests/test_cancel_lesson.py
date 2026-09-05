import requests
import allure
from config import BASE_URL


@allure.title("Отмена созданного урока")
def test_cancel_lesson(auth_headers, created_lesson_id):
    """TC-API-03: Отмена урока"""

    payload = {"id": created_lesson_id, "startAt": "2026-09-10T10:00:00+03:00"}

    response = requests.post(
        f"{BASE_URL}/v2/schedule/removePersonal", headers=auth_headers, json=payload
    )

    assert response.status_code == 200
    json_data = response.json()
    assert json_data.get("errors") is None
    assert json_data["data"] is True

    print(f"🗑️ Урок с ID {created_lesson_id} отменен")
