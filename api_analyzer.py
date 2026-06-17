import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace

def analyze_face(image_bytes):
    """
    Анализирует фото через DeepFace (локально, без внешних ключей).
    Определяет: пол, возраст, расу.
    """
    try:
        # Преобразуем байты в изображение OpenCV
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return {"error": "Не удалось прочитать изображение"}

        # Анализ через DeepFace
        analysis = DeepFace.analyze(img, actions=['age', 'gender', 'race'], enforce_detection=False)
        
        # Берём первый результат (если несколько лиц)
        result = analysis[0] if isinstance(analysis, list) else analysis

        # Извлекаем пол (DeepFace возвращает словарь {'Man': %, 'Woman': %})
        gender_dict = result.get('gender', {})
        if gender_dict:
            gender = max(gender_dict, key=gender_dict.get).lower()
        else:
            gender = 'unknown'

        # Возраст
        age = result.get('age', 30)
        if age < 25:
            age_category = 'young'
        elif age < 45:
            age_category = 'middle'
        else:
            age_category = 'old'

        # Раса
        race_dict = result.get('race', {})
        if race_dict:
            race = max(race_dict, key=race_dict.get).lower()
        else:
            race = 'caucasian'

        # Цвет глаз и волос DeepFace не определяет, оставляем значения по умолчанию
        # Пользователь сможет их уточнить вручную
        return {
            "gender": gender,
            "age_category": age_category,
            "race": race,
            "skin_tone": "medium",   # можно заменить на auto, но пока стандарт
            "hair_color": "brown",   # заглушка
            "eye_color": "brown",    # заглушка
            "face_detected": True
        }
    except Exception as e:
        return {"error": f"Ошибка анализа: {str(e)}"}
