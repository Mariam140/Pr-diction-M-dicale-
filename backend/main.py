from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Charger le modèle et le scaler
model, scaler = joblib.load("main.pkl")

class HeartData(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

app = FastAPI()

@app.post("/predict")
def predict(data: HeartData):
    # Créer un tableau numpy des données reçues
    input_data = np.array([[
        data.age, data.sex, data.cp, data.trestbps, data.chol,
        data.fbs, data.restecg, data.thalach, data.exang, data.oldpeak,
        data.slope, data.ca, data.thal
    ]])
    
    # Appliquer la même normalisation que pendant l'entraînement
    input_scaled = scaler.transform(input_data)
    
    # Faire la prédiction
    prediction = model.predict(input_scaled)[0]
    
    return {"prediction": int(prediction)}
