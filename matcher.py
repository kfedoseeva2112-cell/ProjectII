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

    # Поиск точного совпадения
    for rule in rules:
        match = True
        for key, value in rule.items():
            if key == "рекомендации":
                continue
            if key in features:
                if features[key] != value:
                    match = False
                    break
            if key == "occasion":
                if value != occasion:
                    match = False
                    break
        if match:
            recommendations = rule.get("рекомендации", {})
            # Гарантируем наличие makeup
            if "makeup" not in recommendations or not recommendations["makeup"]:
                recommendations["makeup"] = ["Естественный макияж"]
            return recommendations

    # Поиск по полу + цветотипу + мероприятию
    for rule in rules:
        if (rule.get("gender") == features.get("gender") and
            rule.get("color_type") == features.get("color_type") and
            rule.get("occasion") == occasion):
            recommendations = rule.get("рекомендации", {})
            if "makeup" not in recommendations or not recommendations["makeup"]:
                recommendations["makeup"] = ["Естественный макияж"]
            return recommendations

    # Поиск по полу + мероприятию
    for rule in rules:
        if rule.get("gender") == features.get("gender") and rule.get("occasion") == occasion:
            recommendations = rule.get("рекомендации", {})
            if "makeup" not in recommendations or not recommendations["makeup"]:
                recommendations["makeup"] = ["Естественный макияж"]
            return recommendations

    # Дефолтный ответ с гарантированным makeup
    return {
        "одежда": ["Универсальный комплект", "Базовая вещь", "Аксессуар"],
        "цвета": ["Нейтральные", "Пастельные"],
        "аксессуары": ["Минималистичные"],
        "makeup": ["Естественный макияж"],
        "style_tip": "Подберите свой идеальный образ с нашим стилистом!"
    }
