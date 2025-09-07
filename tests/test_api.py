"""
Тесты для API

Содержит тесты для всех endpoints API.
"""
import requests
import json

BASE_URL = "http://localhost:44445"

def test_api():
    """Тестирует основные endpoints API"""
    
    print("🚀 Тестирование Tickets Booking API")
    print("=" * 50)
    
    # Тест 1: Проверка доступности API
    print("\n1. Проверка доступности API...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ API доступен")
            print(f"   Ответ: {response.json()}")
        else:
            print(f"❌ API недоступен. Статус: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к API. Убедитесь, что сервер запущен.")
        return
    
    # Тест 2: Логин существующего пользователя
    print("\n2. Тестирование логина...")
    login_data = {
        "email": "kate@mail.ru",
        "password": "1111"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ Логин успешен")
            user_data = response.json()
            token = user_data.get("token")
            if token:
                print(f"   Получен токен: {token[:20]}...")
            else:
                print("   Токен не получен")
                return
        else:
            print(f"❌ Ошибка логина: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return
    except Exception as e:
        print(f"❌ Ошибка при логине: {e}")
        return
    
    # Тест 3: Получение информации о пользователе
    print("\n3. Тестирование получения профиля...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            print("✅ Профиль получен успешно")
            print(f"   Пользователь: {response.json()['full_name']}")
        else:
            print(f"❌ Ошибка получения профиля: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка при получении профиля: {e}")
    
    # Тест 4: Получение всех постов
    print("\n4. Тестирование получения постов...")
    try:
        response = requests.get(f"{BASE_URL}/posts/")
        if response.status_code == 200:
            posts = response.json()
            print(f"✅ Получено {len(posts)} постов")
            if posts:
                print(f"   Первый пост: {posts[0]['title']}")
        else:
            print(f"❌ Ошибка получения постов: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка при получении постов: {e}")
    
    # Тест 5: Получение тегов
    print("\n5. Тестирование получения тегов...")
    try:
        response = requests.get(f"{BASE_URL}/posts/tags/")
        if response.status_code == 200:
            tags = response.json()
            print(f"✅ Получено {len(tags)} тегов")
            if tags:
                print(f"   Теги: {', '.join(tags[:5])}")
        else:
            print(f"❌ Ошибка получения тегов: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка при получении тегов: {e}")
    
    # Тест 6: Бронирование билета
    print("\n6. Тестирование бронирования билета...")
    try:
        response = requests.get(f"{BASE_URL}/posts/")
        if response.status_code == 200:
            posts = response.json()
            if posts:
                post_id = posts[0]['post_id']
                booking_data = {"post_id": post_id}
                
                response = requests.post(f"{BASE_URL}/posts/", json=booking_data, headers=headers)
                if response.status_code == 200:
                    print("✅ Билет забронирован успешно")
                    print(f"   Ответ: {response.json()}")
                elif response.status_code == 400:
                    print("⚠️  Билет уже забронирован")
                else:
                    print(f"❌ Ошибка бронирования: {response.status_code}")
                    print(f"   Ответ: {response.text}")
            else:
                print("⚠️  Нет постов для бронирования")
        else:
            print("❌ Не удалось получить посты для тестирования бронирования")
    except Exception as e:
        print(f"❌ Ошибка при бронировании: {e}")
    
    # Тест 7: Получение моих билетов
    print("\n7. Тестирование получения моих билетов...")
    try:
        response = requests.get(f"{BASE_URL}/posts/my-tickets/", headers=headers)
        if response.status_code == 200:
            tickets = response.json()
            print(f"✅ Получено {len(tickets)} билетов")
            if tickets:
                print(f"   Первый билет: {tickets[0]['title']}")
        else:
            print(f"❌ Ошибка получения билетов: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка при получении билетов: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Тестирование завершено!")
    print("\nДля полного тестирования API откройте:")
    print(f"📖 Документация: {BASE_URL}/docs")
    print(f"🔧 ReDoc: {BASE_URL}/redoc")

if __name__ == "__main__":
    test_api()
