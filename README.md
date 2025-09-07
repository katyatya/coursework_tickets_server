# Tickets Booking API

API для бронирования билетов на различные события, построенный на FastAPI с PostgreSQL.

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
