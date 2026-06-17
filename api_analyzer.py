import requests
import streamlit as st

# Забираем ключ из секретов Streamlit (или впиши прямо здесь)
try:
    API_KEY = st.secrets["LUXAND_API_KEY"]
except:
    API_KEY = "ea3b7153b5a3422e84452581fd4ac5b7"  # замени на свой, если нет секретов

def analyze_face(image_bytes):
    """
    Отправляет фото в Luxand API через multipart/form-data,
    возвращает словарь с параметрами или None при ошибке.
    """
    url = "https://api.luxand.cloud/photo/attributes"
    headers = {"token": API_KEY}
    files = {"photo": ("photo.jpg", image_bytes, "image/jpeg")}
    
    try:
        response = requests.post(url, headers=headers, files=files, timeout=10)
        if response.status_code != 200:
            return {"error": f"API вернул {response.status_code}: {response.text}"}
        
        data = response.json()
        # Преобразуем ответ в нужный формат
        result = {
            "gender": data.get("gender", "").lower(),
            "age": data.get("age", ""),
            "skin_tone": data.get("skin_tone", "").lower(),
            "hair_color": data.get("hair_color", "").lower(),
            "eye_color": data.get("eye_color", "").lower(),
            "race": data.get("race", "").lower(),
        }
        # Если нет лица, то будет ошибка
        if not result["gender"] and not result["skin_tone"]:
            return {"error": "Лицо не распознано. Попробуйте другое фото."}
        return result
    except Exception as e:
        return {"error": f"Ошибка соединения: {e}"}
