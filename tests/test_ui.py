import os
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://teachers.skyeng.ru"
SESSION_FILE = "session.json"


@pytest.fixture(scope="function")
def logged_in_page(browser):
    """Открывает страницу с сохранённой сессией"""
    if not os.path.exists(SESSION_FILE):
        pytest.skip(f"⚠️ Файл {SESSION_FILE} не найден. Запусти save_session.py")
    
    context = browser.new_context(storage_state=SESSION_FILE)
    page = context.new_page()
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    
    print(f"📌 URL: {page.url}")
    yield page
    context.close()


def test_schedule_page_loads(logged_in_page: Page):
    """TC-UI-01: Страница расписания загружается"""
    page = logged_in_page
    assert "teachers.skyeng.ru" in page.url
    assert "login" not in page.url


def test_schedule_tab_is_visible(logged_in_page: Page):
    """TC-UI-02: Вкладка «Расписание» отображается"""
    page = logged_in_page
    schedule_tab = page.locator("text=Расписание").first
    expect(schedule_tab).to_be_visible(timeout=15000)

def test_create_lesson_button_is_visible(logged_in_page: Page):
    """TC-UI-03: Элементы управления расписанием отображаются"""
    page = logged_in_page

    buttons = page.locator("button")
    expect(buttons.first).to_be_visible(timeout=15000)

    week_label = page.locator("text=–").first
    expect(week_label).to_be_visible(timeout=15000)

    days_label = page.locator("text=/Пон|Вт|Ср|Чт|Пт|Суб|Вс/").first
    expect(days_label).to_be_visible(timeout=15000)

def test_week_view_is_available(logged_in_page: Page):
    """TC-UI-04: Отображение дней недели в расписании"""
    page = logged_in_page
    
    days = ["Пон", "Вт", "Ср", "Чт", "Пт", "Суб", "Вс"]
    found_day = False
    for day in days:
        if page.locator(f"text={day}").count() > 0:
            found_day = True
            break
    
    assert found_day, "В расписании не найдены дни недели"


def test_page_has_no_critical_errors(logged_in_page: Page):
    """TC-UI-05: На странице нет критических ошибок"""
    page = logged_in_page
    error_locator = page.locator("text=Ошибка").first
    expect(error_locator).not_to_be_visible()
