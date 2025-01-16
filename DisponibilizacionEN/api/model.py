# api/model.py

from transformers import DistilBertTokenizer 
from transformers import DistilBertForSequenceClassification
import torch
import torch.nn.functional as F
import os
import spacy
import re
from nltk.corpus import stopwords
import nltk
from typing import List

class SuicidePredictor:
    def __init__(self, model_path=os.getenv('MODEL_PATH')):
        # Cargar recursos de NLP
        self.nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])
        # Asegurarse de que las stopwords estén descargadas
        try:
            self.english_stopwords = stopwords.words('english')
        except LookupError:
            nltk.download('stopwords')
            self.english_stopwords = stopwords.words('english')
        
        # Cargar el tokenizer
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        
        # Verificar que existe el archivo del modelo
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"No se encontró el archivo del modelo en {model_path}")
        
        # Inicializar la arquitectura del modelo
        self.model = DistilBertForSequenceClassification.from_pretrained(
            'distilbert-base-uncased',
            num_labels=2
        )
        
        # Cargar los pesos del modelo
        state_dict = torch.load(model_path, map_location=torch.device('cpu'), weights_only = True)
        self.model.load_state_dict(state_dict)
        self.model.eval()

    def clean_text_english(self, text: str) -> str:
        # Convertir a minúsculas
        text = text.lower()
        
        # Eliminar stopwords
        text = " ".join([word for word in text.split() if word not in self.english_stopwords])
        
        # Procesar con spaCy
        doc = self.nlp(text)
        
        # Lematización y limpieza de tokens
        cleaned_tokens = [token.lemma_ for token in doc if token.is_alpha and len(token) > 2]
        
        # Eliminar URLs, emails, emojis y caracteres especiales
        cleaned_tokens = [re.sub(r'http\S+|\S+@\S+|[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U0001FB00-\U0001FBFF\U0001FE00-\U0001FE0F\U0001F004]+', '', token) for token in cleaned_tokens]
        cleaned_tokens = [re.sub(r'[^a-zA-Z\s]', '', token).strip() for token in cleaned_tokens]
        cleaned_tokens = [token for token in cleaned_tokens if len(token) > 2]
        
        return ' '.join(cleaned_tokens)

    def predict(self, text: str):
        # Preparar el texto
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )
        
        # Hacer la predicción
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = F.softmax(outputs.logits, dim=1)
            prediction = torch.argmax(probabilities, dim=1)
            confidence = torch.max(probabilities).item()

        return bool(prediction.item()), confidence

    def preprocess_text(self, text: str) -> str:
        """Preprocesa el texto aplicando todas las transformaciones necesarias"""
        return self.clean_text_english(text)
