import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import User, Post
from app.crud.user import create_user
from app.crud.post import create_post
from app.schemas.user import UserCreate
from app.schemas.post import PostCreate

# Create database tables
User.metadata.create_all(bind=engine)
Post.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    try:
        # Create users
        users_data = [
            {
                "full_name": "Kate Ruad",
                "email": "kate@mail.ru",
                "password": "1111"
            },
            {
                "full_name": "Admin",
                "email": "admin2@mail.ru", 
                "password": "1111"
            }
        ]
        
        for user_data in users_data:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing_user:
                user_create = UserCreate(**user_data)
                create_user(db, user_create)
        
        # Create posts
        posts_data = [
            {
                "text": "Профессиональный баскетбольный клуб ЦСКА (Москва) — самый титулованный российский баскетбольный клуб. Поклонников ЦСКА можно считать счастливчиками: они вправе гордиться историей, богаче которой нет практически ни у кого в Европе, вспоминать личностей, ставших олицетворением баскетбола в СССР и России.",
                "title": "Матч ЦСКА 11 декабря 2024",
                "tags": ["футбол"],
                "image_url": "https://cdn.kassir.ru/msk/poster/06/0671f7e179fb5f792efa93ddfc2f222d.jpg",
                "tickets_limit": 50
            },
            {
                "text": "Кубок Легенд 2025: старт продаж билетов 25 ноября! ⚽Февраль 2025 года обещает стать незабываемым для всех поклонников футбола! С 8 по 9 февраля в Москве, в ДС «Мегаспорт», пройдет 17-й Международный футбольный турнир Кубок Легенд имени Константина Еременко.В этом году Кубок Легенд удивит всех: на поле выйдут мировые звезды футбола , некоторые из которых впервые примут участие в турнире. Знаменитые игроки, оставившие яркий след в истории спорта, соберутся в Москве ради красивой игры и захватывающих моментов.",
                "title": "Кубок Легенд 2025 8 февраля 2025",
                "tags": ["футбол"],
                "image_url": "https://cdn.kassir.ru/msk/poster/53/532afcf5867c2a06fa848803cdba12d0.png",
                "tickets_limit": 200
            },
            {
                "text": "В главной схватке вечера сразятся двукратный чемпион России по рукопашному бою и панкратиону, экс боец UFC Омари Ахмедов и действующий боец UFC Денис Тюлюлин.",
                "title": "12-й турнир борцовской лиги WOLNIK",
                "tags": ["борьба"],
                "image_url": "https://cdn.kassir.ru/msk/poster/f9/f9f1740b2baa095c12ac186c2931dc30.jpg",
                "tickets_limit": 30
            },
            {
                "text": "Домашние матчи «Витязя» — это не только хоккей, но и яркое шоу.На наших матчах вы увидите всё: страсть, борьбу, радость и горечь поражений — это настоящий спорт, который никого не оставит равнодушным.",
                "title": "Витязь - Спартак 29 декабря 2024",
                "tags": ["хоккей"],
                "image_url": "https://img.kassir.ru/_qtGXqPJ0PpIJR2Hv46oGWN9FkvbQLK4o_zO-4nz6Ok/aHR0cHM6Ly9jZG4ua2Fzc2lyLnJ1L21zay9nYWxsZXJ5LzUxLzUxMmM0NTM2ZTc5MDk0MzBkZTQ4MzBmNTgyYTg2MDJjLmpwZw.webp",
                "tickets_limit": 150
            },
            {
                "text": "Режиссер, автор инсценировки – Семен ШоминВ роли Владимира Маяковского – Никита Кологривый Почему сгорает человек? Человек талантливый и известный, любимый женщинами и обласканный властями. Как это происходит, какие механизмы внутри человека запускают процесс саморазрушения?",
                "title": "Маяковский. Я сам 5 декабря 2024",
                "tags": ["театр"],
                "image_url": "https://cdn.kassir.ru/msk/poster/1c/1c66fd89247459ef1192a9d018c47106.jpg",
                "tickets_limit": 80
            },
            {
                "text": "Новый год приближается. И какой же зимний праздник без «Щелкунчика», который способен погрузить нас в атмосферу волшебной сказки и дать возможность прикоснуться к чуду, дать надежду на чудо.Сказочный балет-феерию «Щелкунчик» П.И. Чайковского 18 и 19 декабря 2024 года покажет традиционно на сцене Государственного Кремлевского Дворца Академия Русского балета имени А.Я. Вагановой.",
                "title": "«Щелкунчик». Спектакль Академии Русского балета",
                "tags": ["театр"],
                "image_url": "https://cdn.kassir.ru/msk/poster/40/4009af54874b9a88442368887471b8db.jpg",
                "tickets_limit": 5
            }
        ]
        
        for post_data in posts_data:
            # Check if post already exists
            existing_post = db.query(Post).filter(Post.title == post_data["title"]).first()
            if not existing_post:
                post_create = PostCreate(**post_data)
                create_post(db, post_create)
        
        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
