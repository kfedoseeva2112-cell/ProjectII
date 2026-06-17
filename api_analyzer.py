import requests
import streamlit as st
import base64

# --- ВАШИ КЛЮЧИ (уже вставлены) ---
API_KEY = "TJnymPukGSYQIAi_lS3VOtpplaezJEto"
API_SECRET = "WGF2ZgyFB0pWWjZY0C6taq20ROK4fRRH"

def analyze_face(image_bytes):
    """
    Отправляет фото в Face++ API и возвращает параметры внешности.
    """
    url = "https://api-us.faceplusplus.com/facepp/v3/detect"
    
    # Кодируем фото в base64
    encoded = base64.b64encode(image_bytes).decode('utf-8')
    
    params = {
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "image_base64": encoded,
        "return_attributes": "gender,age,race,emotion"
    }
    
    try:
        response = requests.post(url, data=params, timeout=15)
        if response.status_code != 200:
            return {"error": f"API ошибка: {response.status_code}"}
        
        data = response.json()
        if "error_message" in data:
            return {"error": data["error_message"]}
        
        if not data.get("faces"):
            return {"error": "Лицо не найдено на фото. Попробуйте другое фото."}
        
        face = data["faces"][0]
        attrs = face.get("attributes", {})
        
        # Извлекаем параметры
        gender = attrs.get("gender", {}).get("value", "").lower()
        age = attrs.get("age", {}).get("value", 30)
        race = attrs.get("race", {}).get("value", "").lower()
        
        # Категоризируем возраст
        if age < 25:
            age_category = "young"
        elif age < 45:
            age_category = "middle"
        else:
            age_category = "old"
        
        # Маппинг расы (Face++ возвращает свои названия)
        race_map = {
            "asian": "asian",
            "white": "caucasian",
            "black": "african",
            "hispanic": "hispanic"
        }
        race = race_map.get(race, "caucasian")
        
        # Для тона кожи, цвета волос и глаз используем приблизительные значения
        # (их сложно определить по одному фото без дополнительных моделей)
        skin_tone = "medium"
        hair_color = "brown"
        eye_color = "brown"
        
        return {
            "gender": gender,
            "age_category": age_category,
            "race": race,
            "skin_tone": skin_tone,
            "hair_color": hair_color,
            "eye_color": eye_color,
            "face_detected": True
        }
    except Exception as e:
        return {"error": f"Ошибка соединения: {e}"}
