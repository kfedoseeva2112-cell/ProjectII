import random

def analyze_face(image_bytes):
    """
    Имитация работы AI – возвращает случайные параметры внешности.
    Для демонстрации на презентации.
    """
    # Можно задать фиксированный набор для стабильности
    # Но сделаем случайный, чтобы показать разнообразие
    genders = ["female", "male"]
    ages = ["young", "middle", "old"]
    races = ["caucasian", "asian", "african", "hispanic"]
    skin_tones = ["fair", "medium", "dark"]
    hair_colors = ["blond", "brown", "black", "red", "gray"]
    eye_colors = ["blue", "green", "brown", "hazel"]
    
    return {
        "gender": random.choice(genders),
        "age_category": random.choice(ages),
        "race": random.choice(races),
        "skin_tone": random.choice(skin_tones),
        "hair_color": random.choice(hair_colors),
        "eye_color": random.choice(eye_colors),
        "face_detected": True
    }
