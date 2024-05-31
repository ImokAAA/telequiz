from .database import SessionLocal
from .models import User

def save_user_to_db(telegram_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        new_user = User(telegram_id=telegram_id)
        db.add(new_user)
        db.commit()
    db.close()