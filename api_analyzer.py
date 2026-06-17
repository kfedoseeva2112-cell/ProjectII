import hashlib
import random

# Список возможных вариантов параметров (для разных хешей)
PARAM_SETS = [
    {"gender": "female", "age_category": "young", "race": "caucasian", "skin_tone": "fair", "hair_color": "blond", "eye_color": "blue"},
    {"gender": "male", "age_category": "young", "race": "caucasian", "skin_tone": "fair", "hair_color": "brown", "eye_color": "green"},
    {"gender": "female", "age_category": "middle", "race": "asian", "skin_tone": "medium", "hair_color": "black", "eye_color": "brown"},
    {"gender": "male", "age_category": "middle", "race": "caucasian", "skin_tone": "medium", "hair_color": "brown", "eye_color": "hazel"},
    {"gender": "female", "age_category": "young", "race": "african", "skin_tone": "dark", "hair_color": "black", "eye_color": "brown"},
    {"gender": "male", "age_category": "old", "race": "caucasian", "skin_tone": "fair", "hair_color": "gray", "eye_color": "blue"},
    {"gender": "female", "age_category": "old", "race": "hispanic", "skin_tone": "medium", "hair_color": "brown", "eye_color": "brown"},
    {"gender": "male", "age_category": "young", "race": "asian", "skin_tone": "medium", "hair_color": "black", "eye_color": "brown"},
    {"gender": "female", "age_category": "middle", "race": "caucasian", "skin_tone": "fair", "hair_color": "red", "eye_color": "green"},
    {"gender": "male", "age_category": "middle", "race": "african", "skin_tone": "dark", "hair_color": "black", "eye_color": "brown"},
    {"gender": "female", "age_category": "young", "race": "asian", "skin_tone": "fair", "hair_color": "black", "eye_color": "brown"},
    {"gender": "male", "age_category": "old", "race": "asian", "skin_tone": "medium", "hair_color": "gray", "eye_color": "brown"},
]

def analyze_face(image_bytes):
    """
    Определяет параметры внешности на основе хеша изображения.
    Для одного фото результат всегда одинаковый.
    """
    try:
        # Вычисляем MD5-хеш от байтов фото
        md5 = hashlib.md5(image_bytes).hexdigest()
        # Преобразуем первые 8 символов хеша в число
        hash_int = int(md5[:8], 16)
        # Выбираем один из вариантов по индексу
        index = hash_int % len(PARAM_SETS)
        result = PARAM_SETS[index].copy()
        result["face_detected"] = True
        return result
    except Exception as e:
        return {"error": f"Ошибка анализа: {str(e)}"}
