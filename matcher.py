import json
import os

def load_rules():
    """
    Загружает стилистические правила из JSON-файла.
    Ищет файл в папках: data/, корень проекта, Данные/.
    Возвращает список правил. Если файл не найден – возвращает пустой список.
    """
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
                # Если в JSON массив – возвращаем его, иначе оборачиваем в список
                return data if isinstance(data, list) else [data]
    # Если файл не найден – возвращаем пустой список
    return []

def get_recommendations(features, occasion):
    """
    Основная функция сопоставления параметров пользователя с правилами.
    
    Аргументы:
        features (dict): словарь с параметрами внешности. 
                         Ожидаемые ключи: gender, skin_tone, hair_color, eye_color, race, age_category, 
                                         color_type, face_shape, body_type
        occasion (str): мероприятие, выбранное пользователем (например, "Офис", "Свидание").
    
    Возвращает:
        dict: словарь с рекомендациями вида:
              {
                  "одежда": [...],
                  "цвета": [...],
                  "аксессуары": [...],
                  "makeup": [...],
                  "style_tip": "..."
              }
    """
    # Загружаем все правила
    rules = load_rules()
    
    # Если правил нет – возвращаем стандартный базовый набор
    if not rules:
        return {
            "одежда": ["Классический пиджак", "Брюки нейтрального цвета", "Простая блуза"],
            "цвета": ["Серый", "Синий", "Белый"],
            "аксессуары": ["Кожаный ремень", "Сумка-шопер"],
            "makeup": ["Естественный макияж"],
            "style_tip": "Базовый универсальный образ."
        }

    # 1. Ищем точное совпадение всех полей (включая мероприятие)
    for rule in rules:
        match = True
        for key, value in rule.items():
            if key == "рекомендации":
                continue
            # Если ключ есть в features – сравниваем
            if key in features:
                if features[key] != value:
                    match = False
                    break
            # Если ключ "occasion" – сравниваем отдельно
            if key == "occasion":
                if value != occasion:
                    match = False
                    break
        if match:
            # Возвращаем рекомендации из найденного правила
            recommendations = rule.get("рекомендации", {})
            # Гарантируем наличие поля makeup (если его нет, добавляем дефолтное)
            if "makeup" not in recommendations or not recommendations["makeup"]:
                recommendations["makeup"] = ["Естественный макияж"]
            return recommendations

    # 2. Если точного совпадения нет – ищем по полу + цветотипу + мероприятию
    for rule in rules:
        if (rule.get("gender") == features.get("gender") and
            rule.get("color_type") == features.get("color_type") and
            rule.get("occasion") == occasion):
            recommendations = rule.get("рекомендации", {})
            if "makeup" not in recommendations or not recommendations["makeup"]:
                recommendations["makeup"] = ["Естественный макияж"]
            return recommendations

    # 3. Если и такого нет – ищем по полу + мероприятию
    for rule in rules:
        if rule.get("gender") == features.get("gender") and rule.get("occasion") == occasion:
            recommendations = rule.get("рекомендации", {})
            if "makeup" not in recommendations or not recommendations["makeup"]:
                recommendations["makeup"] = ["Естественный макияж"]
            return recommendations

    # 4. Если ничего не подошло – возвращаем дефолтный образ
    return {
        "одежда": ["Универсальный комплект", "Базовая вещь", "Аксессуар"],
        "цвета": ["Нейтральные", "Пастельные"],
        "аксессуары": ["Минималистичные"],
        "makeup": ["Естественный макияж"],
        "style_tip": "Подберите свой идеальный образ с нашим стилистом!"
    }
