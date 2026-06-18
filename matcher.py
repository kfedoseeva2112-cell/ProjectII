import json
import os
import streamlit as st

def load_rules():
    # Пытаемся найти файл в разных местах
    paths = [
        'data/style_rules.json',
        'style_rules.json',
        'Данные/style_rules.json'
    ]
    for path in paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                else:
                    return [data]
    return []

def get_recommendations(features, occasion):
    rules = load_rules()
    # Отладка
    st.write(f"🔍 Загружено правил: {len(rules)}")
    if not rules:
        st.warning("⚠️ Правила не загружены! Возвращаю дефолт.")
        return {
            "одежда": ["Платье-рубашка", "Тренч", "Босоножки"],
            "цвета": ["Персиковый", "Бежевый", "Золотой"],
            "аксессуары": ["Чокер", "Сумка-полумесяц"],
            "makeup": ["Румяна", "Помада нюд"],
            "style_tip": "Нежный и естественный образ для первого свидания."
        }
    
    # Поиск точного совпадения
    for rule in rules:
        match = True
        for key, value in rule.items():
            if key == "рекомендации":
                continue
            # Если ключ есть в features, сравниваем
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
            recommendations = rule.get("рекомендации", {})
            # гарантируем наличие ключей
            recommendations.setdefault("одежда", ["Нет данных"])
            recommendations.setdefault("цвета", ["Нет данных"])
            recommendations.setdefault("аксессуары", ["Нет данных"])
            recommendations.setdefault("makeup", ["Нет данных"])
            recommendations.setdefault("style_tip", "")
            return recommendations
    
    # Если точного нет – ищем по полу + цветотипу + мероприятию
    for rule in rules:
        if (rule.get("gender") == features.get("gender") and
            rule.get("color_type") == features.get("color_type") and
            rule.get("occasion") == occasion):
            recommendations = rule.get("рекомендации", {})
            recommendations.setdefault("одежда", ["Нет данных"])
            recommendations.setdefault("цвета", ["Нет данных"])
            recommendations.setdefault("аксессуары", ["Нет данных"])
            recommendations.setdefault("makeup", ["Нет данных"])
            recommendations.setdefault("style_tip", "")
            return recommendations

    # Если ничего не подошло – возвращаем пример
    return {
        "одежда": ["Универсальный комплект", "Базовая вещь", "Аксессуар"],
        "цвета": ["Нейтральные", "Пастельные"],
        "аксессуары": ["Минималистичные"],
        "makeup": ["Естественный макияж"],
        "style_tip": "Подберите свой идеальный образ с нашим стилистом!"
    }
