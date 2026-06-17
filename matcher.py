import json
import os

def load_rules():
    script_dir = os.path.dirname(__file__)
    json_path = os.path.join(script_dir, 'data', 'style_rules.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Если данные — массив, возвращаем его, иначе оборачиваем
    if isinstance(data, list):
        return data
    else:
        return [data]

def get_recommendations(features):
    """
    features: словарь от api_analyzer (gender, age, skin_tone, hair_color, eye_color, race)
    """
    rules = load_rules()
    # Преобразуем возраст в категорию (можно оставить как есть, но в правилах будем использовать "young", "middle", "old")
    age_str = features.get("age", "")
    if age_str:
        try:
            age_num = int(age_str.split('-')[0])  # берём начало диапазона
            if age_num < 25:
                age_cat = "young"
            elif age_num < 45:
                age_cat = "middle"
            else:
                age_cat = "old"
        except:
            age_cat = "middle"
    else:
        age_cat = "middle"

    # Добавим в features категорию возраста
    features["age_category"] = age_cat

    # Ищем правило, где все поля совпадают (если поле не задано в правиле — пропускаем)
    for rule in rules:
        match = True
        for key, value in rule.items():
            if key == "рекомендации":
                continue
            # Если в правиле есть ключ, проверяем соответствие
            if key in features:
                if features[key] != value:
                    match = False
                    break
        if match:
            return rule.get("рекомендации", {})

    # Если ничего не найдено — возвращаем базовый набор
    return {
        "одежда": ["Классический пиджак", "Брюки нейтрального цвета", "Простая блуза"],
        "цвета": ["Серый", "Синий", "Белый"],
        "аксессуары": ["Кожаный ремень", "Сумка-шопер"],
        "makeup": ["Естественный макияж"],
        "style_tip": "Базовый универсальный образ, подходящий всем."
    }
