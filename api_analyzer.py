import requests
import base64
import json

# --- ВАШИ КЛЮЧИ (замените, если нужно) ---
API_KEY = "TJnymPukGSYQIAi_lS3VOtpplaezJEto"
API_SECRET = "WGF2ZgyFB0pWWjZY0C6taq20ROK4fRRH"

def analyze_face(image_bytes):
    """
    Отправляет фото в Face++ и возвращает параметры.
    Использует двухэтапный подход для обхода ограничений.
    """
    # 1. Детекция лица (без атрибутов)
    url_detect = "https://api-us.faceplusplus.com/facepp/v3/detect"
    encoded = base64.b64encode(image_bytes).decode('utf-8')
    
    payload = {
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "image_base64": encoded,
        "return_landmark": 0,  # не нужны
        "return_attributes": "none"  # не запрашиваем здесь, чтобы избежать ошибки
    }
    
    try:
        resp = requests.post(url_detect, data=payload, timeout=10)
        if resp.status_code != 200:
            return {"error": f"Детекция не удалась: {resp.status_code} - {resp.text}"}
        
        data = resp.json()
        if "error_message" in data:
            return {"error": data["error_message"]}
        
        faces = data.get("faces")
        if not faces:
            return {"error": "Лицо не найдено на фото"}
        
        face_token = faces[0]["face_token"]
        
        # 2. Запрос атрибутов по токену
        url_analyze = "https://api-us.faceplusplus.com/facepp/v3/face/analyze"
        payload_analyze = {
            "api_key": API_KEY,
            "api_secret": API_SECRET,
            "face_tokens": face_token,
            "return_attributes": "gender,age,race"
        }
        resp2 = requests.post(url_analyze, data=payload_analyze, timeout=10)
        if resp2.status_code != 200:
            return {"error": f"Анализ не удался: {resp2.status_code} - {resp2.text}"}
        
        data2 = resp2.json()
        if "error_message" in data2:
            return {"error": data2["error_message"]}
        
        faces2 = data2.get("faces")
        if not faces2:
            return {"error": "Атрибуты не получены"}
        
        attrs = faces2[0].get("attributes", {})
        
        # Извлечение параметров
        gender = attrs.get("gender", {}).get("value", "").lower()
        age = attrs.get("age", {}).get("value", 30)
        race_raw = attrs.get("race", {}).get("value", "").lower()
        
        # Категоризация возраста
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
        
        # Для остальных параметров (тон кожи, цвет волос, глаз) оставляем заглушки,
        # так как Face++ их не выдаёт (можно будет определить отдельно)
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
