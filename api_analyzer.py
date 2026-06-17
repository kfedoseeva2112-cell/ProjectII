import requests
import base64
from PIL import Image
import io

API_KEY = "ea3b7153b5a3422e84452581fd4ac5b7" # Замените на реальный ключ

def analyze_face(image_bytes):
    """
    Отправляет фото в Luxand API и возвращает словарь параметров.
    """
    # Кодируем изображение в base64
    encoded = base64.b64encode(image_bytes).decode('utf-8')
    
    url = "https://api.luxand.cloud/photo/attributes"
    headers = {"token": API_KEY}
    payload = {"photo": encoded}
    
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    if response.status_code != 200:
        return {"error": "Не удалось распознать лицо"}
    
    data = response.json()
    # Извлекаем нужные поля (они приходят в виде строк)
    result = {
        "gender": data.get("gender", "").lower(),          # "male" / "female"
        "age": data.get("age", ""),                        # строка, например "25-35"
        "skin_tone": data.get("skin_tone", "").lower(),    # "fair", "medium", "dark"
        "hair_color": data.get("hair_color", "").lower(),  # "blond", "brown", "black", "red"
        "eye_color": data.get("eye_color", "").lower(),    # "blue", "green", "brown", "hazel"
        "race": data.get("race", "").lower(),              # "caucasian", "asian", "african"
    }
    # Приводим возраст к категориям (можно оставить как есть)
    return result
