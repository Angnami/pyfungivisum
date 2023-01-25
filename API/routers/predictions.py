import sys

sys.path.append("..")

import os, io
from ML.efficientnet import EfficientNetModel
from PIL import Image
from fastapi import File, UploadFile
from database import SessionLocal, engine, get_db
import models
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from .auth import get_current_user
from typing import Optional

models.Base.metadata.create_all(bind=engine)

model = EfficientNetModel('ML/efficientnet_full_model.h5')

router = APIRouter(
    tags=['model']
)

def get_prediction_results(file):
    content = file.file.read()
    image = Image.open(io.BytesIO(content)).convert('RGB')
    output = model.make_prediction(image)
    return output

@router.post('/prediction')
async def make_prediction(presumed_specy: Optional[models.Species] = None,
            user: dict = Depends(get_current_user), db: Session = Depends(get_db), 
            file:UploadFile = File(...)):
    userid = user.get('id')
    if presumed_specy:
        presumedspecy = presumed_specy.value
    else:
        presumedspecy = presumed_specy
    results = get_prediction_results(file=file)
    probability = results.get('confidence')
    specy = results.get('predicted_specy')
    imagename = file.filename
    new_prediction = models.Predictions(imagename=imagename,userid=userid, 
    predictedspecy = specy, presumedspecy=presumedspecy, confidence= probability)
    db.add(new_prediction)
    db.commit()
    results.update({"presumed_specy": presumed_specy})
    return results