import requests
import base64

# --- ВАШИ КЛЮЧИ ---
API_KEY = "TJnymPukGSYQIAi_lS3VOtpplaezJEto"
API_SECRET = "WGF2ZgyFB0pWWjZY0C6taq20ROK4fRRH"

def analyze_face(image_bytes):
    """
    Двухэтапный запрос к Face++:
    1. Детекция лица (без атрибутов) -> получаем face_token.
    2. Анализ атрибутов (gender, age, race) по face_token.
    """
    # --- ШАГ 1: Детекция лица ---
    url_detect = "https://api-us.faceplusplus.com/facepp/v3/detect"
    encoded = base64.b64encode(image_bytes).decode('utf-8')
    params = {
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "image_base64": encoded
    }
    
    try:
        resp = requests.post(url_detect, data=params, timeout=10)
        if resp.status_code != 200:
            return {"error": f"Ошибка детекции: {resp.status_code}"}
        data = resp.json()
        if "error_message" in data:
            return {"error": data["error_message"]}
        if not data.get("faces"):
            return {"error": "Лицо не найдено на фото"}
        
        face_token = data["faces"][0]["face_token"]
        
        # --- ШАГ 2: Получение атрибутов ---
        url_analyze = "https://api-us.faceplusplus.com/facepp/v3/face/analyze"
        params_analyze = {
            "api_key": API_KEY,
            "api_secret": API_SECRET,
            "face_tokens": face_token,
            "return_attributes": "gender,age,race"
        }
        resp2 = requests.post(url_analyze, data=params_analyze, timeout=10)
        if resp2.status_code != 200:
            return {"error": f"Ошибка анализа: {resp2.status_code}"}
        data2 = resp2.json()
        if "error_message" in data2:
            return {"error": data2["error_message"]}
        if not data2.get("faces"):
            return {"error": "Атрибуты не получены"}
        
        attrs = data2["faces"][0].get("attributes", {})
        
        # Извлекаем параметры
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
        
        # Тон кожи, цвет волос и глаз пока оставляем как заглушки
        # (их можно определить дополнительно, но для демонстрации этого достаточно)
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
