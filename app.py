import streamlit as st
from PIL import Image
from api_analyzer import analyze_face
from matcher import get_recommendations

st.set_page_config(
    page_title="StyleMate Pro",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ------------------- ПРЕМИУМ CSS -------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.8rem;
        font-weight: 900;
        text-align: center;
        margin: 0.2rem 0 0.1rem 0;
        letter-spacing: -1px;
        line-height: 1.2;
    }
    
    .sub-header {
        text-align: center;
        color: #6c757d;
        font-size: 1.2rem;
        font-weight: 300;
        margin-bottom: 2rem;
        letter-spacing: 3px;
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 1rem;
    }
    
    .step-box {
        background: white;
        border-radius: 24px;
        padding: 1.8rem 2rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.06);
        margin: 1.5rem 0;
        border: 1px solid #f0f0f0;
        transition: all 0.2s;
    }
    
    .step-box:hover {
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.12);
    }
    
    .step-title {
        font-weight: 700;
        font-size: 1.2rem;
        color: #2d3748;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .param-label {
        font-weight: 500;
        color: #4a5568;
        font-size: 0.9rem;
        margin-bottom: 0.2rem;
    }
    
    .rec-card {
        background: linear-gradient(135deg, #f8faff 0%, #f0f4ff 100%);
        border-radius: 20px;
        padding: 1.5rem 2rem;
        margin: 0.8rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 6px 24px rgba(102, 126, 234, 0.08);
        transition: transform 0.2s;
    }
    
    .rec-card:hover {
        transform: translateY(-4px);
    }
    
    .rec-card h4 {
        color: #2d3748;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .rec-card ul {
        list-style: none;
        padding-left: 0;
        margin: 0;
    }
    
    .rec-card li {
        padding: 0.3rem 0;
        border-bottom: 1px solid #edf2f7;
        font-weight: 400;
        color: #4a5568;
    }
    
    .rec-card li:last-child {
        border-bottom: none;
    }
    
    .tip-box {
        background: #edf2f7;
        border-radius: 16px;
        padding: 1.2rem 1.8rem;
        border-left: 5px solid #f6ad55;
        margin-top: 1.2rem;
        font-style: italic;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 60px;
        padding: 0.7rem 2.5rem;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 36px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Стили для selectbox и полей ввода */
    .stSelectbox > div, .stTextInput > div {
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        transition: border 0.2s;
    }
    
    .stSelectbox > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }
    
    .stFileUploader > div {
        border: 2px dashed #cbd5e0;
        border-radius: 16px;
        padding: 1.5rem;
        transition: background 0.2s;
        background: #f7fafc;
    }
    
    .stFileUploader > div:hover {
        background: #edf2f7;
        border-color: #667eea;
    }
    
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
        margin: 2rem 0;
        opacity: 0.4;
    }
    
    .footer {
        text-align: center;
        color: #a0aec0;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #edf2f7;
    }
    
    @media (max-width: 640px) {
        .main-header { font-size: 2.5rem; }
        .step-box { padding: 1rem; }
    }
</style>
""", unsafe_allow_html=True)

# ------------------- ЗАГОЛОВКИ -------------------
st.markdown('<div class="main-header">StyleMate Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">✨ Ваш персональный AI-стилист с расширенными параметрами</div>', unsafe_allow_html=True)

# ------------------- МАППИНГИ ДЛЯ ВЫВОДА -------------------
gender_map = {"female": "Женский", "male": "Мужской"}
skin_map = {"fair": "Светлая", "medium": "Средняя", "dark": "Тёмная"}
hair_map = {"blond": "Блондин", "brown": "Шатен", "black": "Брюнет", "red": "Рыжий", "gray": "Седой"}
eyes_map = {"blue": "Голубые", "green": "Зелёные", "brown": "Карие", "hazel": "Ореховые"}
race_map = {"caucasian": "Европеец", "asian": "Азиат", "african": "Африканец", "hispanic": "Латиноамериканец"}
age_map = {"young": "Молодой", "middle": "Средний", "old": "Зрелый"}
color_type_map = {"spring": "Весна", "summer": "Лето", "autumn": "Осень", "winter": "Зима"}
face_shape_map = {"oval": "Овал", "round": "Круг", "square": "Квадрат", "triangle": "Треугольник", "diamond": "Ромб"}
body_type_map = {"hourglass": "Песочные часы", "pear": "Груша", "apple": "Яблоко", "rectangle": "Прямоугольник"}

# ------------------- ШАГ 1: ЗАГРУЗКА ФОТО -------------------
st.markdown("---")
st.markdown('<div class="step-title">📸 Шаг 1. Загрузите ваше фото</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ваше фото", use_column_width=True)

    if st.button("🔍 Распознать параметры по фото (автоматически)", type="primary"):
        with st.spinner("Анализируем лицо с помощью AI..."):
            bytes_data = uploaded_file.getvalue()
            features = analyze_face(bytes_data)
            if "error" in features:
                st.error(f"❌ {features['error']}")
            else:
                st.success("✅ Параметры распознаны! Поля ниже автоматически заполнены.")
                st.session_state.features = features
                st.session_state.auto_detected = True

# ------------------- ШАГ 2: ПАРАМЕТРЫ (расширенные) -------------------
st.markdown("---")
st.markdown('<div class="step-title">✏️ Шаг 2. Уточните все параметры внешности</div>', unsafe_allow_html=True)
st.markdown("_Заполните все поля, даже если они уже предзаполнены — это поможет получить максимально точный образ._")

# Получаем значения по умолчанию из сессии (если есть)
default_gender = st.session_state.get("features", {}).get("gender", "female")
default_skin = st.session_state.get("features", {}).get("skin_tone", "fair")
default_hair = st.session_state.get("features", {}).get("hair_color", "blond")
default_eyes = st.session_state.get("features", {}).get("eye_color", "blue")
default_race = st.session_state.get("features", {}).get("race", "caucasian")
default_age = st.session_state.get("features", {}).get("age_category", "young")

# Создаём колонки для компактности
c1, c2 = st.columns(2)

with c1:
    gender = st.selectbox("🧑 Пол", options=list(gender_map.keys()), format_func=lambda x: gender_map[x],
                          index=list(gender_map.keys()).index(default_gender) if default_gender in gender_map else 0,
                          help="Ваш биологический пол")
    skin_tone = st.selectbox("🎨 Тон кожи", options=list(skin_map.keys()), format_func=lambda x: skin_map[x],
                             index=list(skin_map.keys()).index(default_skin) if default_skin in skin_map else 0,
                             help="Цвет кожи для подбора оттенков")
    hair_color = st.selectbox("💇‍♀️ Цвет волос", options=list(hair_map.keys()), format_func=lambda x: hair_map[x],
                              index=list(hair_map.keys()).index(default_hair) if default_hair in hair_map else 0,
                              help="Естественный цвет волос")
    # НОВЫЙ ПАРАМЕТР: Цветотип
    color_type = st.selectbox("🌈 Ваш цветотип", options=list(color_type_map.keys()), format_func=lambda x: color_type_map[x],
                              index=0, help="Определите, к какому сезону относится ваша внешность (поможет с палитрой)")

with c2:
    age_category = st.selectbox("📅 Возрастная категория", options=list(age_map.keys()), format_func=lambda x: age_map[x],
                                index=list(age_map.keys()).index(default_age) if default_age in age_map else 0,
                                help="Ваш возрастной диапазон")
    eye_color = st.selectbox("👁️ Цвет глаз", options=list(eyes_map.keys()), format_func=lambda x: eyes_map[x],
                             index=list(eyes_map.keys()).index(default_eyes) if default_eyes in eyes_map else 0,
                             help="Цвет радужки")
    race = st.selectbox("🌍 Раса", options=list(race_map.keys()), format_func=lambda x: race_map[x],
                        index=list(race_map.keys()).index(default_race) if default_race in race_map else 0,
                        help="Этническая принадлежность для учета особенностей")
    # НОВЫЙ ПАРАМЕТР: Форма лица
    face_shape = st.selectbox("🔷 Форма лица", options=list(face_shape_map.keys()), format_func=lambda x: face_shape_map[x],
                              index=0, help="Форма вашего лица для подбора аксессуаров и причесок")
    # НОВЫЙ ПАРАМЕТР: Тип фигуры
    body_type = st.selectbox("🧍 Тип фигуры", options=list(body_type_map.keys()), format_func=lambda x: body_type_map[x],
                             index=0, help="Тип телосложения для рекомендаций по крою одежды")

# ------------------- ШАГ 3: МЕРОПРИЯТИЕ -------------------
st.markdown("---")
st.markdown('<div class="step-title">📅 Шаг 3. Выберите случай</div>', unsafe_allow_html=True)
occasion = st.selectbox(
    "Для какого мероприятия подбираем образ?",
    options=["Офис", "Свидание", "Вечеринка", "Прогулка", "Спорт", "Деловая встреча", "Свадьба", "Отдых"],
    index=0,
    key="occasion_select",
    help="От этого зависит стиль и формальность наряда"
)
st.session_state.occasion = occasion

# ------------------- КНОПКА ПОДБОРА -------------------
st.markdown("---")
if st.button("✨ Подобрать идеальный образ!", type="primary", use_container_width=True):
    # Собираем все параметры в словарь
    features_full = {
        "gender": gender,
        "skin_tone": skin_tone,
        "hair_color": hair_color,
        "eye_color": eye_color,
        "race": race,
        "age_category": age_category,
        "color_type": color_type,
        "face_shape": face_shape,
        "body_type": body_type
    }
    # Получаем рекомендации
    recommendations = get_recommendations(features_full, occasion)

    # ------------------- ВЫВОД РЕЗУЛЬТАТА (КРАСИВО) -------------------
    st.markdown("---")
    st.markdown('<div class="step-title">🌟 Ваш персональный образ готов!</div>', unsafe_allow_html=True)

    # Разбиваем на две колонки
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 👗 Одежда")
        rec_clothes = recommendations.get("одежда", [])
        if rec_clothes:
            st.markdown('<div class="rec-card"><ul>' + ''.join([f'<li>{item}</li>' for item in rec_clothes]) + '</ul></div>', unsafe_allow_html=True)
        else:
            st.info("Нет рекомендаций по одежде")

        st.markdown("#### 🎨 Цветовая палитра")
        rec_colors = recommendations.get("цвета", [])
        if rec_colors:
            st.markdown('<div class="rec-card"><ul>' + ''.join([f'<li>{item}</li>' for item in rec_colors]) + '</ul></div>', unsafe_allow_html=True)
        else:
            st.info("Нет рекомендаций по цветам")

    with col_right:
        st.markdown("#### 💍 Аксессуары")
        rec_accessories = recommendations.get("аксессуары", [])
        if rec_accessories:
            st.markdown('<div class="rec-card"><ul>' + ''.join([f'<li>{item}</li>' for item in rec_accessories]) + '</ul></div>', unsafe_allow_html=True)
        else:
            st.info("Нет рекомендаций по аксессуарам")

        st.markdown("#### 💄 Макияж")
        rec_makeup = recommendations.get("makeup", [])
        if rec_makeup:
            st.markdown('<div class="rec-card"><ul>' + ''.join([f'<li>{item}</li>' for item in rec_makeup]) + '</ul></div>', unsafe_allow_html=True)
        else:
            st.info("Нет рекомендаций по макияжу")

    # Совет стилиста
    tip = recommendations.get("style_tip", "")
    if tip:
        st.markdown(f'<div class="tip-box">💡 <strong>Совет стилиста:</strong> {tip}</div>', unsafe_allow_html=True)

    # Дополнительно показываем все введённые параметры (для наглядности)
    with st.expander("📋 Параметры, которые вы указали"):
        st.json(features_full)

# ------------------- ПОДВАЛ -------------------
st.markdown("---")
with st.expander("ℹ️ Как это работает"):
    st.markdown("""
    **StyleMate Pro** анализирует ваше фото через локальную нейросеть (DeepFace) и определяет пол, возраст и расу.
    Вы также можете ввести все параметры вручную — цветотип, форму лица, тип фигуры и другие.
    На основе ваших данных и базы стилистических правил мы подбираем идеальный образ с учётом мероприятия.
    """)
st.markdown('<div class="footer">© 2026 StyleMate Pro — создано с ❤️ для вашего стиля</div>', unsafe_allow_html=True)
