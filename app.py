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

# ------------------- СЛОЖНЫЙ ПРЕМИУМ CSS -------------------
st.markdown("""
<style>
    /* Импорт шрифтов и иконок */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');

    * {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
    }

    /* Анимированный градиентный фон для всей страницы */
    .stApp {
        background: linear-gradient(-45deg, #f8faff, #eef2ff, #fdf2f8, #f0f4ff);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Стеклянная карточка (glassmorphism) */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 32px;
        padding: 2rem 2.2rem;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.08), 0 8px 20px rgba(0, 0, 0, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin: 1.2rem 0;
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        box-shadow: 0 30px 60px rgba(102, 126, 234, 0.15);
        transform: translateY(-4px);
    }

    /* Заголовок с неоновым свечением */
    .main-title {
        font-size: 4.2rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 40%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(102, 126, 234, 0.2);
        letter-spacing: -2px;
        margin-bottom: 0.2rem;
        line-height: 1.1;
        animation: glowPulse 3s ease-in-out infinite;
    }

    @keyframes glowPulse {
        0%, 100% { text-shadow: 0 0 30px rgba(102, 126, 234, 0.2); }
        50% { text-shadow: 0 0 60px rgba(102, 126, 234, 0.4); }
    }

    .sub-title {
        text-align: center;
        font-size: 1.1rem;
        font-weight: 300;
        color: #6c7a9a;
        letter-spacing: 4px;
        border-bottom: 2px solid rgba(102, 126, 234, 0.2);
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Индикатор шагов (прогресс-бар) */
    .step-progress {
        display: flex;
        justify-content: space-between;
        margin: 1.5rem 0 2rem 0;
        position: relative;
    }

    .step-progress::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 3px;
        background: #e2e8f0;
        transform: translateY(-50%);
        z-index: 0;
    }

    .step-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        flex: 1;
        position: relative;
        z-index: 1;
    }

    .step-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: white;
        border: 3px solid #cbd5e0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: #4a5568;
        transition: all 0.4s ease;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }

    .step-circle.active {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-color: #667eea;
        color: white;
        transform: scale(1.1);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }

    .step-circle.done {
        background: #667eea;
        border-color: #667eea;
        color: white;
    }

    .step-label {
        margin-top: 8px;
        font-size: 0.75rem;
        font-weight: 600;
        color: #4a5568;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .step-label.active {
        color: #667eea;
    }

    /* Стилизованные поля ввода */
    .stSelectbox > div, .stTextInput > div, .stFileUploader > div {
        border-radius: 16px !important;
        border: 2px solid #e2e8f0 !important;
        transition: all 0.3s ease !important;
        background: rgba(255,255,255,0.6) !important;
        backdrop-filter: blur(4px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }

    .stSelectbox > div:focus-within, .stTextInput > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15) !important;
        background: white !important;
    }

    .stFileUploader > div {
        border: 2px dashed #cbd5e0 !important;
        background: rgba(247, 250, 252, 0.7) !important;
        padding: 1.8rem !important;
        text-align: center;
    }

    .stFileUploader > div:hover {
        border-color: #667eea !important;
        background: rgba(102, 126, 234, 0.04) !important;
    }

    /* Кнопки с анимацией и неоном */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border: none;
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.75rem 2.5rem;
        border-radius: 60px;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
        width: 100%;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 60%);
        opacity: 0;
        transition: opacity 0.4s;
        transform: scale(0.5);
    }

    .stButton > button:hover::after {
        opacity: 1;
        transform: scale(1);
    }

    .stButton > button:hover {
        transform: scale(1.03) translateY(-2px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
    }

    .stButton > button:active {
        transform: scale(0.97);
    }

    /* Карточки рекомендаций с иконками и цветными границами */
    .rec-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.2rem;
        margin: 1rem 0;
    }

    .rec-card {
        background: white;
        border-radius: 24px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
        border-left: 6px solid #667eea;
        transition: all 0.3s ease;
        backdrop-filter: blur(4px);
        background: rgba(255, 255, 255, 0.8);
    }

    .rec-card:hover {
        transform: translateY(-6px) scale(1.01);
        box-shadow: 0 16px 40px rgba(102, 126, 234, 0.12);
    }

    .rec-card h4 {
        font-size: 1rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .rec-card ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .rec-card li {
        padding: 0.4rem 0;
        border-bottom: 1px solid #edf2f7;
        font-weight: 400;
        color: #4a5568;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .rec-card li:last-child {
        border-bottom: none;
    }

    .rec-card li::before {
        content: "•";
        color: #667eea;
        font-weight: 900;
        font-size: 1.2rem;
    }

    /* Цветовая палитра в виде квадратов */
    .color-swatch-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin: 0.5rem 0;
    }

    .color-swatch {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 2px solid white;
        transition: transform 0.2s;
    }

    .color-swatch:hover {
        transform: scale(1.12);
    }

    /* Совет стилиста с кавычками */
    .tip-box {
        background: linear-gradient(135deg, #faf5ff, #f3e8ff);
        border-radius: 20px;
        padding: 1.5rem 2rem;
        border-left: 8px solid #f6ad55;
        margin: 1.5rem 0;
        font-style: italic;
        font-weight: 500;
        color: #4a3a5c;
        position: relative;
    }

    .tip-box::before {
        content: "“";
        font-size: 3rem;
        color: #f6ad55;
        position: absolute;
        top: -10px;
        left: 12px;
        opacity: 0.3;
    }

    /* Параметры, которые указал пользователь – в виде красивых тегов */
    .param-tag {
        display: inline-block;
        background: #edf2f7;
        border-radius: 30px;
        padding: 0.2rem 1rem;
        font-size: 0.8rem;
        font-weight: 600;
        color: #2d3748;
        margin: 0.2rem 0.2rem;
        border: 1px solid #e2e8f0;
        transition: all 0.2s;
    }

    .param-tag:hover {
        background: #667eea;
        color: white;
        border-color: #667eea;
    }

    /* Анимация появления */
    .fade-in {
        animation: fadeInUp 0.7s ease both;
    }

    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* Отдельный блок для цветотипа */
    .season-badge {
        display: inline-block;
        padding: 0.4rem 1.2rem;
        border-radius: 40px;
        font-weight: 700;
        font-size: 0.9rem;
        background: linear-gradient(135deg, #f6ad55, #ed8936);
        color: white;
        box-shadow: 0 4px 12px rgba(237, 137, 54, 0.3);
    }

    /* Разделитель с иконкой */
    .divider {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 2rem 0;
        color: #a0aec0;
        font-size: 0.8rem;
        gap: 1rem;
    }

    .divider::before, .divider::after {
        content: '';
        flex: 1;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }

    /* Адаптив */
    @media (max-width: 640px) {
        .main-title { font-size: 2.8rem; }
        .glass-card { padding: 1.2rem; }
        .rec-grid { grid-template-columns: 1fr; }
        .step-progress { flex-direction: column; gap: 0.8rem; }
        .step-item { flex-direction: row; gap: 0.8rem; justify-content: flex-start; }
        .step-circle { width: 32px; height: 32px; font-size: 0.8rem; }
    }
</style>
""", unsafe_allow_html=True)

# ------------------- ЗАГОЛОВОК -------------------
st.markdown('<div class="main-title">StyleMate Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">✨ ИИ-стилист с премиум-анализом</div>', unsafe_allow_html=True)

# ------------------- ИНДИКАТОР ШАГОВ -------------------
# Определяем текущий шаг (можно сделать динамическим позже)
step = 1
if "features" in st.session_state and st.session_state.get("auto_detected", False):
    step = 2
if "recommendations_done" in st.session_state:
    step = 3

st.markdown(f"""
<div class="step-progress">
    <div class="step-item">
        <div class="step-circle { 'active' if step>=1 else '' }">1</div>
        <div class="step-label { 'active' if step>=1 else '' }">Фото</div>
    </div>
    <div class="step-item">
        <div class="step-circle { 'active' if step>=2 else '' }">2</div>
        <div class="step-label { 'active' if step>=2 else '' }">Параметры</div>
    </div>
    <div class="step-item">
        <div class="step-circle { 'active' if step>=3 else '' }">3</div>
        <div class="step-label { 'active' if step>=3 else '' }">Образ</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------- МАППИНГИ -------------------
gender_map = {"female": "👩 Женский", "male": "👨 Мужской"}
skin_map = {"fair": "☀️ Светлая", "medium": "🌤️ Средняя", "dark": "🌙 Тёмная"}
hair_map = {"blond": "💛 Блондин", "brown": "🤎 Шатен", "black": "🖤 Брюнет", "red": "❤️ Рыжий", "gray": "🤍 Седой"}
eyes_map = {"blue": "💙 Голубые", "green": "💚 Зелёные", "brown": "🤎 Карие", "hazel": "🧡 Ореховые"}
race_map = {"caucasian": "🌍 Европеец", "asian": "🌏 Азиат", "african": "🌍 Африканец", "hispanic": "🌎 Латиноамериканец"}
age_map = {"young": "🧑 Молодой", "middle": "👨 Средний", "old": "🧓 Зрелый"}
color_type_map = {"spring": "🌸 Весна", "summer": "☀️ Лето", "autumn": "🍂 Осень", "winter": "❄️ Зима"}
face_shape_map = {"oval": "🥚 Овал", "round": "⭕ Круг", "square": "⬛ Квадрат", "triangle": "🔻 Треугольник", "diamond": "💎 Ромб"}
body_type_map = {"hourglass": "⌛ Песочные часы", "pear": "🍐 Груша", "apple": "🍎 Яблоко", "rectangle": "📏 Прямоугольник"}

# ------------------- ШАГ 1: ЗАГРУЗКА ФОТО -------------------
st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
st.markdown("#### 📸 Шаг 1. Загрузите ваше фото")

uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ваше фото", use_column_width=True)

    if st.button("🔍 Распознать параметры по фото", type="primary"):
        with st.spinner("Анализируем лицо с помощью AI..."):
            bytes_data = uploaded_file.getvalue()
            features = analyze_face(bytes_data)
            if "error" in features:
                st.error(f"❌ {features['error']}")
            else:
                st.success("✅ Параметры распознаны! Поля ниже автоматически заполнены.")
                st.session_state.features = features
                st.session_state.auto_detected = True
                st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# ------------------- ШАГ 2: ПАРАМЕТРЫ -------------------
st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
st.markdown("#### ✏️ Шаг 2. Уточните все параметры внешности")
st.markdown("_Чем точнее вы заполните, тем лучше будет результат._")

default_gender = st.session_state.get("features", {}).get("gender", "female")
default_skin = st.session_state.get("features", {}).get("skin_tone", "fair")
default_hair = st.session_state.get("features", {}).get("hair_color", "blond")
default_eyes = st.session_state.get("features", {}).get("eye_color", "blue")
default_race = st.session_state.get("features", {}).get("race", "caucasian")
default_age = st.session_state.get("features", {}).get("age_category", "young")

c1, c2 = st.columns(2)

with c1:
    gender = st.selectbox("Пол", options=list(gender_map.keys()), format_func=lambda x: gender_map[x],
                          index=list(gender_map.keys()).index(default_gender) if default_gender in gender_map else 0)
    skin_tone = st.selectbox("Тон кожи", options=list(skin_map.keys()), format_func=lambda x: skin_map[x],
                             index=list(skin_map.keys()).index(default_skin) if default_skin in skin_map else 0)
    hair_color = st.selectbox("Цвет волос", options=list(hair_map.keys()), format_func=lambda x: hair_map[x],
                              index=list(hair_map.keys()).index(default_hair) if default_hair in hair_map else 0)
    color_type = st.selectbox("Цветотип", options=list(color_type_map.keys()), format_func=lambda x: color_type_map[x],
                              index=0)

with c2:
    age_category = st.selectbox("Возрастная категория", options=list(age_map.keys()), format_func=lambda x: age_map[x],
                                index=list(age_map.keys()).index(default_age) if default_age in age_map else 0)
    eye_color = st.selectbox("Цвет глаз", options=list(eyes_map.keys()), format_func=lambda x: eyes_map[x],
                             index=list(eyes_map.keys()).index(default_eyes) if default_eyes in eyes_map else 0)
    race = st.selectbox("Раса", options=list(race_map.keys()), format_func=lambda x: race_map[x],
                        index=list(race_map.keys()).index(default_race) if default_race in race_map else 0)
    face_shape = st.selectbox("Форма лица", options=list(face_shape_map.keys()), format_func=lambda x: face_shape_map[x],
                              index=0)
    body_type = st.selectbox("Тип фигуры", options=list(body_type_map.keys()), format_func=lambda x: body_type_map[x],
                             index=0)

# Выбор мероприятия
st.markdown("#### 📅 Шаг 3. Выберите случай")
occasion = st.selectbox(
    "Для какого мероприятия подбираем образ?",
    options=["Офис", "Свидание", "Вечеринка", "Прогулка", "Спорт", "Деловая встреча", "Свадьба", "Отдых"],
    index=0,
    key="occasion_select"
)
st.session_state.occasion = occasion

st.markdown('</div>', unsafe_allow_html=True)

# ------------------- КНОПКА ПОДБОРА -------------------
if st.button("✨ Создать идеальный образ", type="primary", use_container_width=True):
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
    recommendations = get_recommendations(features_full, occasion)
    st.session_state.recommendations = recommendations
    st.session_state.features_full = features_full
    st.session_state.recommendations_done = True
    st.rerun()

# ------------------- ВЫВОД РЕЗУЛЬТАТА -------------------
if "recommendations" in st.session_state:
    rec = st.session_state.recommendations
    features_full = st.session_state.features_full

    st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
    st.markdown("#### 🌟 Ваш персональный образ готов!")

    # Бейдж цветотипа
    season_emoji = {"spring": "🌸", "summer": "☀️", "autumn": "🍂", "winter": "❄️"}
    st.markdown(f"<div style='display:flex; gap:10px; flex-wrap:wrap; margin-bottom:1rem;'>"
                f"<span class='season-badge'>{season_emoji.get(color_type, '')} {color_type_map.get(color_type, '')}</span>"
                f"</div>", unsafe_allow_html=True)

    # Сетка рекомендаций
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 👗 Одежда")
        if rec.get("одежда"):
            st.markdown(f"""
            <div class="rec-card">
                <ul>
                    {''.join([f'<li>{item}</li>' for item in rec["одежда"]])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Нет рекомендаций")

        st.markdown("#### 🎨 Цветовая палитра")
        if rec.get("цвета"):
            # Показываем как квадраты
            colors_html = "<div class='color-swatch-container'>"
            for color in rec["цвета"]:
                # Преобразуем название цвета в hex (приблизительно)
                color_hex = {
                    "белый": "#FFFFFF", "черный": "#000000", "серый": "#808080",
                    "синий": "#007BFF", "голубой": "#87CEEB", "лавандовый": "#B39DDB",
                    "розовый": "#FF69B4", "красный": "#DC3545", "бордовый": "#800020",
                    "зеленый": "#28A745", "оливковый": "#808000", "мятный": "#98FF98",
                    "желтый": "#FFC107", "золотой": "#FFD700", "бежевый": "#F5F5DC",
                    "оранжевый": "#FD7E14", "персиковый": "#FFDAB9", "терракотовый": "#CC7A4B",
                    "вишневый": "#800020", "изумрудный": "#50C878", "бирюзовый": "#40E0D0",
                    "фиолетовый": "#8A2BE2", "сиреневый": "#C8A2C8", "серебро": "#C0C0C0"
                }.get(color.lower(), "#6C63FF")
                colors_html += f"<div class='color-swatch' style='background:{color_hex};'></div>"
            colors_html += "</div>"
            st.markdown(colors_html, unsafe_allow_html=True)
        else:
            st.info("Нет рекомендаций")

    with col_right:
        st.markdown("#### 💍 Аксессуары")
        if rec.get("аксессуары"):
            st.markdown(f"""
            <div class="rec-card">
                <ul>
                    {''.join([f'<li>{item}</li>' for item in rec["аксессуары"]])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Нет рекомендаций")

        st.markdown("#### 💄 Макияж")
        if rec.get("makeup"):
            st.markdown(f"""
            <div class="rec-card">
                <ul>
                    {''.join([f'<li>{item}</li>' for item in rec["makeup"]])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Нет рекомендаций")

    # Совет стилиста
    if rec.get("style_tip"):
        st.markdown(f"""
        <div class="tip-box">
            <strong>💡 Совет стилиста:</strong> {rec['style_tip']}
        </div>
        """, unsafe_allow_html=True)

    # Параметры, которые были введены (визуализация)
    with st.expander("📋 Ваши параметры (для справки)"):
        tags = ""
        for k, v in features_full.items():
            if k in ["gender", "skin_tone", "hair_color", "eye_color", "race", "age_category"]:
                display_map = {
                    "gender": gender_map, "skin_tone": skin_map, "hair_color": hair_map,
                    "eye_color": eyes_map, "race": race_map, "age_category": age_map
                }
                if k in display_map and v in display_map[k]:
                    label = display_map[k][v]
                else:
                    label = v
            elif k == "color_type":
                label = color_type_map.get(v, v)
            elif k == "face_shape":
                label = face_shape_map.get(v, v)
            elif k == "body_type":
                label = body_type_map.get(v, v)
            else:
                label = v
            tags += f"<span class='param-tag'>{k}: {label}</span>"
        st.markdown(tags, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------- ПОДВАЛ -------------------
st.markdown("---")
with st.expander("ℹ️ Как это работает"):
    st.markdown("""
    **StyleMate Pro** использует передовые алгоритмы компьютерного зрения и стилистические правила.
    Вы загружаете фото, система определяет параметры внешности, а затем на основе ваших данных и выбранного мероприятия подбирает идеальный образ.

    **Технологии:**
    - Распознавание лиц: DeepFace (локально)
    - База стилистических правил: более 40 комбинаций
    - Интерфейс: Streamlit с кастомным CSS
    """)
st.markdown('<div style="text-align:center; color:#a0aec0; font-size:0.8rem; margin-top:1rem;">© 2026 StyleMate Pro — создано с ❤️ для вашего стиля</div>', unsafe_allow_html=True)
