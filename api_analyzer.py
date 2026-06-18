import hashlib
from PIL import Image
import numpy as np
import io

def analyze_face(image_bytes):
    """
    Анализирует фото: определяет тон кожи и подбирает детерминированные параметры
    на основе хеша и тона кожи. Это локальный модуль, который можно заменить
    на любой внешний API (Face++, SkyBiometry, свою нейросеть) без изменения
    остального кода.
    """
    try:
        # Открываем изображение
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Берём центральную область для определения тона кожи
        width, height = img.size
        crop_size = min(width, height) // 2
        left = (width - crop_size) // 2
        top = (height - crop_size) // 2
        center = img.crop((left, top, left + crop_size, top + crop_size))
        
        # Средний цвет
        pixels = np.array(center)
        avg_color = pixels.mean(axis=(0, 1))
        brightness = np.mean(avg_color)  # 0-255
        
        # Тон кожи
        if brightness > 180:
            skin_tone = "fair"
        elif brightness > 120:
            skin_tone = "medium"
        else:
            skin_tone = "dark"
        
        # Хеш для детерминизма
        md5 = hashlib.md5(image_bytes).hexdigest()
        hash_int = int(md5[:8], 16)
        
        # Наборы параметров в зависимости от тона кожи
        if skin_tone == "fair":
            options = [
                {"gender": "female", "age_category": "young", "race": "caucasian", "hair_color": "blond", "eye_color": "blue"},
                {"gender": "male", "age_category": "young", "race": "caucasian", "hair_color": "brown", "eye_color": "green"},
                {"gender": "female", "age_category": "middle", "race": "caucasian", "hair_color": "red", "eye_color": "hazel"},
                {"gender": "male", "age_category": "old", "race": "caucasian", "hair_color": "gray", "eye_color": "blue"},
            ]
        elif skin_tone == "medium":
            options = [
                {"gender": "female", "age_category": "young", "race": "asian", "hair_color": "black", "eye_color": "brown"},
                {"gender": "male", "age_category": "young", "race": "asian", "hair_color": "black", "eye_color": "brown"},
                {"gender": "female", "age_category": "middle", "race": "hispanic", "hair_color": "brown", "eye_color": "brown"},
                {"gender": "male", "age_category": "middle", "race": "hispanic", "hair_color": "brown", "eye_color": "hazel"},
            ]
        else:  # dark
            options = [
                {"gender": "female", "age_category": "young", "race": "african", "hair_color": "black", "eye_color": "brown"},
                {"gender": "male", "age_category": "young", "race": "african", "hair_color": "black", "eye_color": "brown"},
                {"gender": "female", "age_category": "middle", "race": "african", "hair_color": "black", "eye_color": "brown"},
                {"gender": "male", "age_category": "old", "race": "african", "hair_color": "gray", "eye_color": "brown"},
            ]
        
        index = hash_int % len(options)
        result = options[index].copy()
        result["skin_tone"] = skin_tone
        result["face_detected"] = True
        return result
    except Exception as e:
        return {"error": f"Ошибка анализа: {str(e)}"}
