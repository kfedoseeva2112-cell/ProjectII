import json
import os

def load_rules():
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
                return data if isinstance(data, list) else [data]
    return []

def get_recommendations(features, occasion):
    rules = load_rules()
    if not rules:
        return {
            "одежда": ["Классический пиджак", "Брюки нейтрального цвета", "Простая блуза"],
            "цвета": ["Серый", "Синий", "Белый"],
            "аксессуары": ["Кожаный ремень", "Сумка-шопер"],
            "makeup": ["Естественный макияж"],
            "style_tip": "Базовый универсальный образ."
        }
    
    # Ищем правило, где совпадают: пол, цвет кожи, возраст, раса И МЕРОПРИЯТИЕ
    for rule in rules:
        match = True
        for key, value in rule.items():
            if key == "рекомендации":
                continue
            # Сравниваем только те поля, которые есть в features
            if key in features:
                if features[key] != value:
                    match = False
                    break
            # Если в правиле есть поле "occasion", оно должно совпадать
            if key == "occasion":
                if value != occasion:
                    match = False
                    break
        if match:
            return rule.get("рекомендации", {})
    
    # Если точного совпадения нет, ищем только по полу и мероприятию
    for rule in rules:
        if rule.get("gender") == features["gender"] and rule.get("occasion") == occasion:
            return rule.get("рекомендации", {})
    
    # Совсем ничего не нашли — возвращаем дефолт
    return {
        "одежда": ["Универсальный комплект", "Базовая вещь", "Аксессуар"],
        "цвета": ["Нейтральные", "Пастельные"],
        "аксессуары": ["Минималистичные"],
        "makeup": ["Естественный"],
        "style_tip": "Подберите свой идеальный образ с нашим стилистом!"
    }
