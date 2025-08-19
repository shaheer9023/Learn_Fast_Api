from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import User, get_session
from auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])





# Create
@router.post("/")
def create_user(user: User, session: Session = Depends(get_session), _: str = Depends(get_current_user)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Read all
@router.get("/")
def get_users(session: Session = Depends(get_session), _: str = Depends(get_current_user)):
    return session.exec(select(User)).all()

# Read one
@router.get("/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_session), _: str = Depends(get_current_user)):
    return session.get(User, user_id)

# Update
@router.put("/{user_id}")
def update_user(user_id: int, updated_user: User, session: Session = Depends(get_session), _: str = Depends(get_current_user)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = updated_user.username
    db_user.password = updated_user.password
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

# Delete
@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session), _: str = Depends(get_current_user)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(db_user)
    session.commit()
    return {"message": "User deleted"}
