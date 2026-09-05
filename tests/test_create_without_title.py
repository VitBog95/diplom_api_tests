import requests
import allure
from config import BASE_URL


@allure.title("Негативный тест: Создание урока без поля title")
def test_create_lesson_without_title(auth_headers):
    """Создание урока без обязательного поля title"""

    payload = {
        "backgroundColor": "#FFF7C7",
        "color": "#FAC641",
        "startAt": "2026-09-10T10:00:00+03:00",
        "endAt": "2026-09-10T11:00:00+03:00",
    }

    response = requests.post(
        f"{BASE_URL}/v2/schedule/createPersonal", headers=auth_headers, json=payload
    )

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["data"] is None
    assert json_data.get("errors") is not None
    assert any(error.get("property") == "title" for error in json_data["errors"])

    print("✅ Негативный тест пройден: ошибка валидации title")
