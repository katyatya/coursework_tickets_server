# Tickets Booking API

API для бронирования билетов на различные события, построенный на FastAPI с PostgreSQL.

## 🏗️ Архитектура

```
server/
├── app/                        # Основное приложение
│   ├── __init__.py
│   ├── main.py                 # FastAPI приложение
│   ├── database.py             # Настройка БД
│   │
│   ├── api/                    # API роутеры
│   │   ├── __init__.py
│   │   ├── deps.py             # Зависимости (auth, db)
│   │   └── v1/                 # Версия API
│   │       ├── __init__.py
│   │       ├── auth.py         # Аутентификация
│   │       └── posts.py        # Посты/события
│   │
│   ├── core/                   # Основная логика
│   │   ├── __init__.py
│   │   ├── config.py           # Настройки
│   │   └── security.py         # JWT, хеширование
│   │
│   ├── models/                 # SQLAlchemy модели
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── post.py
│   │
│   ├── schemas/                # Pydantic схемы
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── auth.py
│   │
│   └── crud/                   # CRUD операции
│       ├── __init__.py
│       ├── base.py             # Базовый CRUD
│       ├── user.py
│       └── post.py
│
├── scripts/                    # Скрипты
│   └── seed.py                 # Заполнение БД
│
├── tests/                      # Тесты
│   └── __init__.py
│
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── run.py                      # Точка входа
```

## 🚀 Установка и запуск

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка базы данных
Создайте файл `.env`:
```env
POSTGRES_URL=postgresql://postgres:password@localhost:5432/tickets_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Заполнение базы данных
```bash
python scripts/seed.py
```

### 4. Запуск сервера
```bash
python run.py
```

Сервер будет доступен по адресу: http://localhost:44445

## 📚 API Endpoints

### Аутентификация
- `POST /auth/register` - Регистрация пользователя
- `POST /auth/login` - Вход в систему
- `GET /auth/me` - Информация о текущем пользователе

### Посты/События
- `GET /posts/` - Получение всех постов
- `GET /posts/{post_id}` - Получение конкретного поста
- `GET /posts/tags/{tag_name}` - Посты по тегу
- `GET /posts/tags` - Популярные теги
- `POST /posts/` - Бронирование билета
- `DELETE /posts/` - Отмена бронирования
- `GET /posts/my-tickets` - Мои билеты
- `POST /posts/upload` - Загрузка файла

## 🔧 Особенности архитектуры

### 1. **Разделение ответственности**
- **Models**: SQLAlchemy модели для работы с БД
- **Schemas**: Pydantic схемы для валидации данных
- **CRUD**: Операции с базой данных
- **API**: HTTP endpoints и бизнес-логика

### 2. **Безопасность**
- JWT токены для аутентификации
- Bcrypt для хеширования паролей
- CORS настройки

### 3. **Масштабируемость**
- Модульная структура
- Версионирование API
- Базовый CRUD класс для переиспользования

### 4. **Типизация**
- Полная типизация с Pydantic
- Автодокументация API
- Валидация данных

## 🧪 Тестирование

```bash
# Тест корневого endpoint
curl http://localhost:44445/

# Тест логина
curl -X POST http://localhost:44445/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "kate@mail.ru", "password": "1111"}'

# Тест бронирования
curl -X POST http://localhost:44445/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"post_id": 1}'
```

## 📝 Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `POSTGRES_URL` | URL базы данных PostgreSQL | `postgresql://postgres:@localhost:5432/tickets_db` |
| `SECRET_KEY` | Секретный ключ для JWT | `secret123` |
| `ALGORITHM` | Алгоритм шифрования JWT | `HS256` |
| `ACCESS_TOKEN_EXMIRE_MINUTES` | Время жизни токена (минуты) | `30` |

## 🔄 Миграция с предыдущей версии

Старые файлы (`config.py`, `models.py`, `schemas.py`, `auth.py`, `crud.py`, `main.py`) были удалены и заменены новой модульной структурой. Все функциональности сохранены, но теперь организованы по принципу разделения ответственности.