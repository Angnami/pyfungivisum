from fastapi import FastAPI
from database import engine
from routers import predictions, auth
import models
import uvicorn

app = FastAPI(
title="PyFungiVisum", 
description='''Cette application permet aux utilisateurs identifiés de charger l'image 
d'un champignon et récevoir une prédiction de son espèce assortie d'une probabilité de prédiction. 
Le modèle est limité uniquement à 15 spèces de champignons à savoir : Amanita flavoconia ,Amanita muscaria,
Baorangia bicolor, Boletus edulis, Coprinus comatus, Galerina marginata, Ganoderma applanatum, Hypholoma fasciculare,
Laetiporus sulphureus, Phaeolus schweinitzii, Pleurotus ostreatus, Pluteus cervinus, Psathyrella candolleana,
Psilocybe cyanescens, Psilocybe zapotecorum'''
)

models.Base.metadata.create_all(bind=engine)


@app.get("/", tags=['home'])
async def welcome():

    return {"message": "Welcome to the PyFungiVisum application!"}


app.include_router(auth.router)
app.include_router(predictions.router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=9000)
