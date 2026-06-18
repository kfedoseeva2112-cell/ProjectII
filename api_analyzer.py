import requests

# --- ВАШИ КЛЮЧИ ---
API_KEY = "TJnymPukGSYQIAi_lS3VOtpplaezJEto"
API_SECRET = "WGF2ZgyFB0pWWjZY0C6taq20ROK4fRRH"

def analyze_face(image_bytes):
    """
    Отправляет фото в Face++ через multipart/form-data.
    Двухэтапный процесс: сначала детекция, затем получение атрибутов.
    """
    # ШАГ 1: Детекция лица (без атрибутов)
    url_detect = "https://api-us.faceplusplus.com/facepp/v3/detect"
    files = {
        "image_file": ("photo.jpg", image_bytes, "image/jpeg")
    }
    data_detect = {
        "api_key": API_KEY,
        "api_secret": API_SECRET,
        "return_attributes": "none"  # на этом этапе не запрашиваем
    }
    
    try:
        resp = requests.post(url_detect, files=files, data=data_detect, timeout=10)
        if resp.status_code != 200:
            return {"error": f"Детекция не удалась: {resp.status_code} - {resp.text}"}
        
        result = resp.json()
        if "error_message" in result:
            return {"error": result["error_message"]}
        
        faces = result.get("faces")
        if not faces:
            return {"error": "Лицо не найдено на фото"}
        
        face_token = faces[0]["face_token"]
        
        # ШАГ 2: Получение атрибутов по токену
        url_analyze = "https://api-us.faceplusplus.com/facepp/v3/face/analyze"
        data_analyze = {
            "api_key": API_KEY,
            "api_secret": API_SECRET,
            "face_tokens": face_token,
            "return_attributes": "gender,age,race"
        }
        resp2 = requests.post(url_analyze, data=data_analyze, timeout=10)
        if resp2.status_code != 200:
            return {"error": f"Анализ не удался: {resp2.status_code} - {resp2.text}"}
        
        result2 = resp2.json()
        if "error_message" in result2:
            return {"error": result2["error_message"]}
        
        faces2 = result2.get("faces")
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
        
        # Остальные параметры (Face++ не определяет их, оставляем заглушки)
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
        return {"error": f"Ошибка соединения: {str(e)}"}
