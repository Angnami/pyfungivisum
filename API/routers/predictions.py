import sys

sys.path.append("..")

import os, io
from ML.efficientnet import EfficientNetModel
from PIL import Image
from fastapi import File, UploadFile
from database.database import SessionLocal, engine, get_db
import models
from fastapi import Depends, APIRouter, Form
from sqlalchemy.orm import Session
from .auth import get_current_user
from typing import Optional
import uuid
from sqlalchemy import text

models.Base.metadata.create_all(bind=engine)
conn = engine.connect()

model = EfficientNetModel('ML/efficientnet_full_model.h5')

router = APIRouter(
    tags=['predictions']
)

def get_prediction_results(file):
    content = file.file.read()
    image = Image.open(io.BytesIO(content)).convert('RGB')
    output = model.make_prediction(image)
    return output

@router.post('/new_prediction')
async def make_prediction(presumed_specy: models.Species= Form(default = None, 
    description="Select a specy from the list if you know it."),
    user: dict = Depends(get_current_user), db: Session = Depends(get_db), 
    file:UploadFile = File(description="Select a mushroom image and get a prediction of it is specy.")):

    userid = user.get('id')
    if presumed_specy:
        presumedspecy = presumed_specy.value
    else:
        presumedspecy = presumed_specy
    
    results = get_prediction_results(file=file)
    results.update({"presumed_specy": presumed_specy})
    probability = results.get('confidence')
    specy = results.get('predicted_specy')
    imagename = file.filename
    new_prediction = models.Predictions(id=uuid.uuid4(),imagename=imagename,userid=userid, 
    predictedspecy = specy, presumedspecy=presumedspecy, confidence= probability)

    db.add(new_prediction)
    db.commit()
    return results


@router.get('/existing_predictions')
async def show_predictions(user:dict = Depends(get_current_user), db: Session = Depends(get_db)):
    pred = db.query(models.Predictions).filter(models.Predictions.userid == user.get('id')).all()
    if len(pred) > 0 :
        return pred
    return {"message": "You didn't make predictions yet. You can upload images and get predictions!"}


@router.delete('/deletion')
async def delete_predictions(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    pred = db.query(models.Predictions).filter(models.Predictions.userid == user.get('id')).all()
    if len(pred) >0 :
        id = user.get('id')
        db.query(models.Predictions).filter(models.Predictions.userid == id).delete()
        db.commit()
        return {"message": "All your predictions are deleted. You can upload other images."}
    return {"message": "You didn't make predictions yet. You can upload images and get predictions!"}