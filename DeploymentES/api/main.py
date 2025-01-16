# api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .model import SuicidePredictor
import torch
import os
from dotenv import load_dotenv
#import logging

# Cargar variables de entorno
load_dotenv()

# Obtener la ruta del modelo desde las variables de entorno
MODEL_PATH = os.getenv('MODEL_PATH')

app = FastAPI(
    title="API de Predicción de Textos Suicidas",
    description="API para detectar textos con contenido suicida"
)

# Inicializar el modelo
try:
    model = SuicidePredictor(model_path=MODEL_PATH)
except Exception as e:
    print(f"Error al cargar el modelo: {str(e)}")
    raise

class TextInput(BaseModel):
    text: str

class PredictionOutput(BaseModel):
    text: str
    is_suicidal: bool
    confidence: float

@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: TextInput):
    try:
    
        prediction, confidence = model.predict(input_data.text)
        
        return {
            "text": input_data.text,
            "is_suicidal": prediction,
            "confidence": confidence
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": True}