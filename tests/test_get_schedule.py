import requests
from config import BASE_URL


def test_get_schedule(auth_headers):
    """TC-API-02: Получение списка событий за период"""

    payload = {"from": "2026-09-01T00:00:00+03:00", "till": "2026-09-07T23:59:59+03:00"}

    response = requests.post(
        f"{BASE_URL}/v2/schedule/events", headers=auth_headers, json=payload
    )

    assert response.status_code == 200
    json_data = response.json()
    assert json_data.get("errors") is None
    assert json_data["data"] is not None
    assert "events" in json_data["data"]

    print(f"✅ Найдено событий: {len(json_data['data']['events'])}")
