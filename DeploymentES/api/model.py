# api/model.py

import os
import torch
from torch.nn import functional as F
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

class SuicidePredictor:
    def __init__(self, model_path=os.getenv('MODEL_PATH')):
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-multilingual-cased')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Modelo no encontrado en {model_path}")
        
        self.model = DistilBertForSequenceClassification.from_pretrained(
            'distilbert-base-multilingual-cased',
            num_labels=2,
            ignore_mismatched_sizes=True
        )
    
        state_dict = torch.load(model_path, map_location=torch.device('cpu'), weights_only=True)
        self.model.load_state_dict(state_dict)
        self.model.eval()

    def predict(self, text: str):
        # Minimal preprocessing
        if not text or text.isspace():
            raise ValueError("El texto está vacío o solo contiene espacios en blanco")
            
        # Handle basic encoding issues (optional but recommended)
        text = text.encode('utf-8', errors='ignore').decode('utf-8')
        
        # Let the tokenizer handle everything else
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = F.softmax(outputs.logits, dim=1)
            prediction = torch.argmax(probabilities, dim=1)
            confidence = torch.max(probabilities).item()

        return bool(prediction.item()), confidence
