"""
Скрипт для обновления базы данных

Добавляет колонку tickets_limit в таблицу posts
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import text
from app.database import engine

def update_database():
    """Обновление структуры базы данных"""
    try:
        with engine.connect() as connection:
            # Добавляем колонку tickets_limit если её нет
            connection.execute(text("""
                ALTER TABLE posts 
                ADD COLUMN IF NOT EXISTS tickets_limit INTEGER DEFAULT 100 NOT NULL;
            """))
            connection.commit()
            print("✅ Колонка tickets_limit добавлена успешно!")
            
    except Exception as e:
        print(f"❌ Ошибка при обновлении базы данных: {e}")

if __name__ == "__main__":
    update_database()
