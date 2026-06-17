import requests
import streamlit as st

# --- ВАШИ КЛЮЧИ ---
API_KEY = "TJnymPukGSYQIAi_lS3VOtpplaezJEto"
API_SECRET = "WGF2ZgyFB0pWWjZY0C6taq20ROK4fRRH"

def analyze_face(image_bytes):
    """
    Отправляет фото в Face++ через multipart/form-data.
    """
    url = "https://api-us.faceplusplus.com/facepp/v3/detect"
    
    # Отправляем файл как есть
    files = {
        "image_file": ("photo.jpg", image_bytes, "image/jpeg")
    }
    data = {
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "return_attributes": "gender,age,race"
    }
    
    try:
        response = requests.post(url, files=files, data=data, timeout=15)
        
        # --- ДЛЯ ОТЛАДКИ: выводим статус и текст ответа ---
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code != 200:
            return {"error": f"API ошибка: {response.status_code} - {response.text}"}
        
        result = response.json()
        if "error_message" in result:
            return {"error": result["error_message"]}
        
        faces = result.get("faces")
        if not faces:
            return {"error": "Лицо не найдено на фото. Попробуйте другое фото."}
        
        face = faces[0]
        attrs = face.get("attributes", {})
        
        # Извлекаем параметры
        gender = attrs.get("gender", {}).get("value", "").lower()
        age = attrs.get("age", {}).get("value", 30)
        race_raw = attrs.get("race", {}).get("value", "").lower()
        
        # Категоризируем возраст
        if age < 25:
            age_category = "young"
        elif age < 45:
            age_category = "middle"
        else:
            age_category = "old"
        
        # Маппинг расы
        race_map = {
            "asian": "asian",
            "white": "caucasian",
            "black": "african",
            "hispanic": "hispanic"
        }
        race = race_map.get(race_raw, "caucasian")
        
        # Для остальных параметров используем заглушки (или можно определить дополнительно)
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
