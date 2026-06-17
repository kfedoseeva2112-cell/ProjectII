import json
import os

def load_rules():
    # Пытаемся найти style_rules.json в папке data
    script_dir = os.path.dirname(__file__)
    possible_paths = [
        os.path.join(script_dir, 'data', 'style_rules.json'),
        os.path.join(script_dir, 'style_rules.json'),
        os.path.join(script_dir, 'Данные', 'style_rules.json'),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                else:
                    return [data]
    # Если ничего не найдено, возвращаем пустой список
    return []

def get_recommendations(features):
    """
    features: словарь с ключами gender, skin_tone, hair_color, eye_color, race, age_category
    """
    rules = load_rules()
    if not rules:
        # Если правил нет, выдаём дефолтный ответ
        return {
            "одежда": ["Классический пиджак", "Брюки нейтрального цвета", "Простая блуза"],
            "цвета": ["Серый", "Синий", "Белый"],
            "аксессуары": ["Кожаный ремень", "Сумка-шопер"],
            "makeup": ["Естественный макияж"],
            "style_tip": "Базовый универсальный образ."
        }
    
    # Преобразуем возраст в категорию, если её нет
    if "age_category" not in features and "age" in features:
        age_str = features["age"]
        try:
            age_num = int(age_str.split('-')[0])
            if age_num < 25:
                features["age_category"] = "young"
            elif age_num < 45:
                features["age_category"] = "middle"
            else:
                features["age_category"] = "old"
        except:
            features["age_category"] = "middle"
    
    # Ищем правило с полным совпадением всех полей, которые есть в features
    for rule in rules:
        match = True
        for key, value in rule.items():
            if key == "рекомендации":
                continue
            # Если в правиле есть ключ, который есть в features, сравниваем
            if key in features:
                if features[key] != value:
                    match = False
                    break
        if match:
            return rule.get("рекомендации", {})
    
    # Если точного совпадения нет, ищем частичное (например, по полу и возрасту)
    # Можно вернуть дефолт
    return {
        "одежда": ["Универсальный комплект", "Базовая вещь", "Аксессуар"],
        "цвета": ["Нейтральные", "Пастельные"],
        "аксессуары": ["Минималистичные"],
        "makeup": ["Естественный"],
        "style_tip": "Подберите свой идеальный образ с нашим стилистом!"
    }
