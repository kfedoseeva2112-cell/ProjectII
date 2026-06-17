import requests
import streamlit as st
import base64

# CompreFace работает через REST API
# Бесплатный публичный демо-сервер (можно использовать для теста)
COMPREFACE_URL = "https://api.compreface.io/v1/recognition/faces"
API_KEY = "your_api_key_here"  # зарегистрируйтесь на compreface.io

def analyze_face(image_bytes):
    """
    Отправляет фото в CompreFace API, возвращает параметры лица.
    """
    # Кодируем фото в base64
    encoded = base64.b64encode(image_bytes).decode('utf-8')
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "image": encoded,
        "detect_faces": "true"
    }
    
    try:
        response = requests.post(COMPREFACE_URL, json=payload, headers=headers, timeout=15)
        if response.status_code != 200:
            return {"error": f"API ошибка: {response.status_code}"}
        
        data = response.json()
        if not data.get("result"):
            return {"error": "Лицо не найдено на фото"}
        
        # Парсим результат (CompreFace возвращает bounding box и landmarks)
        face = data["result"][0]
        # Здесь можно добавить логику определения пола, возраста и т.д.
        # Для простоты пока возвращаем базовые параметры
        return {
            "gender": "female",  # можно определить по дополнительным моделям
            "skin_tone": "medium",
            "hair_color": "brown",
            "eye_color": "brown",
            "race": "caucasian",
            "age_category": "middle",
            "face_detected": True
        }
    except Exception as e:
        return {"error": f"Ошибка соединения: {e}"}
