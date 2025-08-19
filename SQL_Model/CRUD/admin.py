from sqlmodel import Session
from database import engine, User, create_db

def create_admin():
    create_db()  # tables ensure kare
    with Session(engine) as session:
        admin = User(username="shaheerahmad9023@gmail.com", password="4414")
        session.add(admin)
        session.commit()
        session.refresh(admin)
    print("Created admin:", admin.id, admin.username)

if __name__ == "__main__":
    create_admin()
