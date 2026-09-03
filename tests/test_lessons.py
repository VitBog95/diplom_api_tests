import requests
from config import BASE_URL

# =====================================================
# TC-API-01: Создание урока
# =====================================================
def test_create_lesson(auth_headers):
    """Создание урока с валидными данными"""
    
    payload = {
        "backgroundColor": "#FFF7C7",
        "color": "#FAC641",
        "title": "Автотест: Урок с учеником",
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
    
    print(f"✅ Урок создан с ID: {json_data['data']['payload']['id']}")

# =====================================================
# TC-API-03: Отмена урока (использует фикстуру)
# =====================================================
def test_cancel_lesson(auth_headers, created_lesson_id):
    """Отмена созданного урока"""
    
    payload = {
        "id": created_lesson_id,
        "startAt": "2026-09-10T10:00:00+03:00"
    }
    
    response = requests.post(
        f"{BASE_URL}/v2/schedule/removePersonal",
        headers=auth_headers,
        json=payload
    )
    
    assert response.status_code == 200
    json_data = response.json()
    assert json_data.get("errors") is None
    assert json_data["data"] is True
    
    print(f"🗑️ Урок с ID {created_lesson_id} отменен")


# =====================================================
# TC-API-04: Негативный тест (без поля title)
# =====================================================

def test_create_lesson_without_title(auth_headers):
    """Создание урока без обязательного поля title"""
    
    payload = {
        "backgroundColor": "#FFF7C7",
        "color": "#FAC641",
        "startAt": "2026-09-10T10:00:00+03:00",
        "endAt": "2026-09-10T11:00:00+03:00"
        # title отсутствует!
    }
    
    response = requests.post(
        f"{BASE_URL}/v2/schedule/createPersonal",
        headers=auth_headers,
        json=payload
    )
    
    assert response.status_code == 200
    json_data = response.json()
    

    assert json_data["data"] is None
    
    assert json_data.get("errors") is not None
    errors = json_data["errors"]
    
    title_error_found = False
    for error in errors:
        if error.get("property") == "title":
            title_error_found = True
            break
    
    assert title_error_found, "Ожидалась ошибка для поля title"
    
    print("✅ Негативный тест пройден: ошибка валидации title")

# =====================================================
# TC-API-05: Негативный тест (без токена)
# =====================================================
def test_create_lesson_without_token():
    """Создание урока без заголовка Cookie (без авторизации)"""
    
    payload = {
        "backgroundColor": "#FFF7C7",
        "color": "#FAC641",
        "title": "Урок без токена",
        "startAt": "2026-09-10T10:00:00+03:00",
        "endAt": "2026-09-10T11:00:00+03:00"
    }
    

    response = requests.post(
        f"{BASE_URL}/v2/schedule/createPersonal",
        json=payload
    )
    
 
    assert response.status_code == 401
    
    json_data = response.json()
    assert json_data.get("code") == 401
    assert "Authentication required" in json_data.get("message", "")
    
    print("✅ Негативный тест пройден: 401 Unauthorized")