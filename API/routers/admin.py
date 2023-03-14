import sys
sys.path.append("..")

from fastapi import APIRouter, Depends,HTTPException, status
from database.database import get_db, engine, SessionLocal
import models
from sqlalchemy.orm import Session
from sqlalchemy import  text
from .auth import get_current_user
import numpy as np

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    tags = ["admin"]
)

admins = ["Goudja", "Daniel"]
conn = engine.connect()

@router.post("/database")
async def reset_table(table:str, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.get("username") in admins:
        query = text("""
                SELECT users.id  FROM users 
                WHERE users.is_admin='false'
                """
                )
        results = conn.execute(query)
        to_delete= [row[0] for row in results]
        if str.lower(table) =="predictions":
            pred = db.query(models.Predictions).all()
            if len(pred)>0:
                db.query(models.Predictions).filter(models.Predictions.userid.in_(to_delete)).delete()
                db.commit()
                return {"message":f"The {table} table is successfully reset."}
            return {"message":f"Sorry the {table} table is empty."}
        if str.lower(table) == 'users':
            if len(to_delete) > 0:
                db.query(models.Users).filter(models.Users.id.in_(to_delete)).delete()
                db.commit()
                return {"message":f"The {table} table is successfully reset."}
            return {"message":f"Sorry the {table} table is empty."}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sorry you don't have administrator rights!")

@router.delete('/users/remove')
async def delete_user(id:str, user:dict = Depends(get_current_user),
db: Session = Depends(get_db)):
    if user.get("username") in admins:
        to_delete = db.query(models.Users).filter(models.Users.id == id).all()
        if len(to_delete) > 0:
            db.query(models.Users).filter(models.Users.id == id).delete()
            db.commit()
            return {"message": f"User with id {id} is sucessfully deleted."}
        return {"message": f"There is no user with id {id}."}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sorry you don't have administrator rights!")

@router.get('/users/show')
async def show_users(user:dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.get("username") in admins:
        to_show = db.query(models.Users).all()
        if len(to_show) > 0:
            return {"users": to_show}
        return {"message": "There is no regsitred user."}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sorry you don't have administrator rights!")

        


