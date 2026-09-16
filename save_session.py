from playwright.sync_api import sync_playwright

BASE_URL = "https://teachers.skyeng.ru"

with sync_playwright() as p:
    # Открываем видимый браузер, чтобы можно было войти вручную
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    print("🌐 Открываем Skyeng...")
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")

    print("=" * 60)
    print("🔑 Войди в аккаунт ВРУЧНУЮ в открывшемся браузере.")
    print("   Логин: test.tst320@skyeng.ru")
    print("   1. Введи логин и пароль")
    print("   2. Нажми «Войти» (если потребуется — введи код)")
    print("   3. Дождись загрузки расписания")
    print("=" * 60)
    print("⏳ Когда увидишь расписание — вернись сюда и нажми ENTER.")
    input()

    print(f"📌 Итоговый URL: {page.url}")

    context.storage_state(path="session.json")
    print("✅ Сессия сохранена в файл session.json")

    browser.close()