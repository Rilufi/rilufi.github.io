#!/usr/bin/env python
# coding=utf-8

import os
import sys
import json
import urllib.request
import requests
from datetime import datetime, timezone, timedelta
from PIL import Image
import google.generativeai as genai
from pytube import YouTube

# Configurações
API_KEY = os.environ.get("API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
MODEL = genai.GenerativeModel('gemini-1.5-flash')

# Diretórios
ASSETS_DIR = "assets/img"
DATA_DIR = "data"
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

def get_apod_data(date=None):
    """Obtém os dados da APOD para uma data específica ou para hoje"""
    URL_APOD = "https://api.nasa.gov/planetary/apod"
    params = {
        'api_key': API_KEY,
        'hd': 'True',
        'thumbs': 'True',
    }
    
    if date:
        params['date'] = date
    
    response = requests.get(URL_APOD, params=params)
    response.raise_for_status()
    return response.json()

def download_media(apod_data):
    """Baixa a mídia (imagem ou thumbnail do vídeo)"""
    media_type = apod_data.get('media_type')
    url = apod_data.get('url')
    thumbs = apod_data.get('thumbnail_url')
    
    if media_type == 'image':
        media_url = url
#        ext = os.path.splitext(media_url)[1].lower()
#        filename = f"apod{ext}"
         filename = "apod_image.jpg"
    elif media_type == 'video':
        media_url = thumbs
        filename = "apod_image.jpg"
    else:
        raise ValueError("Tipo de mídia não suportado")
    
    # Baixa a mídia
    filepath = os.path.join(ASSETS_DIR, filename)
    urllib.request.urlretrieve(media_url, filepath)
    
    # Se for imagem, verifica e converte se necessário
    if media_type == 'image':
        try:
            img = Image.open(filepath)
            if img.mode == 'P':
                img = img.convert('RGB')
                img.save(filepath)
        except Exception as e:
            print(f"Erro ao processar imagem: {e}")
    
    return filename

def translate_text(text, target_language="pt-BR"):
    """Traduz o texto usando a API Gemini"""
    try:
        prompt = f"Translate the following astronomy-related text to {target_language}, keeping the technical and scientific terms accurate. Return only the translation:\n\n{text}"
        response = MODEL.generate_content(prompt)
        
        if response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        return None
    except Exception as e:
        print(f"Erro ao traduzir texto: {e}")
        return None

def save_apod_info(apod_data, translated_explanation):
    """Salva as informações da APOD em um arquivo JSON"""
    info = {
        "date": apod_data.get('date'),
        "title": apod_data.get('title'),
        "explanation": {
            "en": apod_data.get('explanation'),
            "pt-BR": translated_explanation
        },
        "url": apod_data.get('url'),
        "media_type": apod_data.get('media_type'),
        "hdurl": apod_data.get('hdurl'),
        "thumbnail_url": apod_data.get('thumbnail_url'),
        "copyright": apod_data.get('copyright', '')
    }
    
    # Formata o nome do arquivo com a data
#    date_str = apod_data.get('date').replace('-', '')
    filename = f"apod_today.json"
    filepath = os.path.join(DATA_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    
    return filename

def main(date=None):
    try:
        # Obtém os dados da APOD
        apod_data = get_apod_data(date)
        
        # Baixa a mídia
        media_filename = download_media(apod_data)
        print(f"Mídia salva em: {os.path.join(ASSETS_DIR, media_filename)}")
        
        # Traduz a explicação
        original_explanation = apod_data.get('explanation')
        translated_explanation = translate_text(original_explanation)
        
        if not translated_explanation:
            print("Não foi possível obter a tradução. Usando apenas o texto original.")
            translated_explanation = None
        
        # Salva as informações em JSON
        json_filename = save_apod_info(apod_data, translated_explanation)
        print(f"Informações salvas em: {os.path.join(DATA_DIR, json_filename)}")
        
        return {
            "media_path": os.path.join(ASSETS_DIR, media_filename),
            "json_path": os.path.join(DATA_DIR, json_filename),
            "apod_data": apod_data
        }
        
    except Exception as e:
        print(f"Erro ao processar APOD: {e}")
        return None

if __name__ == "__main__":
    # Pode ser executado com uma data específica (formato YYYY-MM-DD) ou sem argumentos para pegar a do dia
    date = sys.argv[1] if len(sys.argv) > 1 else None
    main(date)
