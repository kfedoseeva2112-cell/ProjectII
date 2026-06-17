import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
import face_recognition

def analyze_face(image_bytes):
    """
    Анализирует фото локально через DeepFace.
    Возвращает словарь с параметрами или None при ошибке.
    """
    try:
        # Преобразуем байты в изображение OpenCV
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return {"error": "Не удалось прочитать изображение"}

        # Проверяем, есть ли лицо
        face_locations = face_recognition.face_locations(img)
        if not face_locations:
            return {"error": "Лицо не найдено. Попробуйте другое фото."}

        # Анализируем через DeepFace (возраст, пол, раса, эмоции)
        analysis = DeepFace.analyze(img, actions=['age', 'gender', 'race'], enforce_detection=False)
        
        # Берём первый результат (если несколько лиц — берём первое)
        result = analysis[0] if isinstance(analysis, list) else analysis

        # Извлекаем параметры
        gender = result.get('gender', '')
        # DeepFace возвращает словарь {'Man': %, 'Woman': %}, берём ключ с большим значением
        if isinstance(gender, dict):
            gender = max(gender, key=gender.get)
        gender = gender.lower()

        age = result.get('age', 30)
        # Категоризируем возраст
        if age < 25:
            age_category = 'young'
        elif age < 45:
            age_category = 'middle'
        else:
            age_category = 'old'

        race_dict = result.get('race', {})
        if race_dict:
            race = max(race_dict, key=race_dict.get).lower()
        else:
            race = 'caucasian'

        # Определяем цвет глаз и волос пока не можем, оставим запасные значения
        # Для демонстрации можно добавить логику по среднему цвету
        # Но проще дать пользователю выбрать вручную, если нужно

        # Возвращаем то, что получили
        return {
            "gender": gender,
            "age_category": age_category,
            "race": race,
            "skin_tone": "medium",  # можно вычислить по цвету кожи, но для простоты оставим
            "hair_color": "brown",  # аналогично
            "eye_color": "brown",
            "face_detected": True
        }
    except Exception as e:
        return {"error": f"Ошибка анализа: {str(e)}"}
