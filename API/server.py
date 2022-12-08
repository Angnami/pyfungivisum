# Importing dependencies
import os, io
from efficientnet import EfficientNetModel
from PIL import Image
from fastapi import FastAPI, Request, File, UploadFile

# Loading the model from efficientnet.py
model = EfficientNetModel('efficientnet_full_model.h5')

# Creating the fastapi application

app = FastAPI(
    title='pyfungivisum',
    version='0.1.0',
    description='This application allows you to predict the specy of a given mushroom.'
)

# Welcome message 
@app.get('/')
def welcome():
    return {'message':'Welcome to the pyfungivisum API!'}

# Creating a route to allow to client to send request
@app.post('/predict',name='Prediction')
def predict_specy(request:Request,file:UploadFile = File(...)):
    content = file.file.read()
    image = Image.open(io.BytesIO(content)).convert('RGB')
    output = model.make_prediction(image)
    return output
