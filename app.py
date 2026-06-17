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

# ------------------- СУПЕР-ПРЕМИУМ CSS С ФОНОВЫМИ ЭЛЕМЕНТАМИ -------------------
st.markdown("""
<style>
    /* Импорт шрифтов */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');

    * {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

    /* Основной контейнер – делаем его прозрачным, фон будет под ним */
    .stApp {
        background: transparent !important;
    }

    /* Настоящий фон с анимированными элементами */
    body::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: -2;
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
        background-size: 400% 400%;
        animation: gradientBG 20s ease infinite;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Анимированные круги – парят в фоне */
    body::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: -1;
        background-image:
            radial-gradient(circle at 10% 20%, rgba(102, 126, 234, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 90% 80%, rgba(118, 75, 162, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(240, 147, 251, 0.1) 0%, transparent 70%);
        background-repeat: no-repeat;
        animation: floatBubbles 15s ease-in-out infinite alternate;
    }

    @keyframes floatBubbles {
        0% { background-position: 10% 20%, 90% 80%, 50% 50%; }
        50% { background-position: 30% 40%, 70% 60%, 40% 70%; }
        100% { background-position: 50% 30%, 50% 90%, 60% 40%; }
    }

    /* Добавляем абстрактные линии-сетку поверх фона */
    .grid-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background-image:
            linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
        background-size: 60px 60px;
        pointer-events: none;
    }

    /* Плавающие геометрические фигуры (SVG) – вставляем как дополнительные элементы */
    .floating-shapes {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        pointer-events: none;
        overflow: hidden;
    }

    .floating-shapes div {
        position: absolute;
        display: block;
        opacity: 0.1;
        animation: floatShape 25s linear infinite;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.4), transparent 70%);
        width: 300px;
        height: 300px;
        top: -150px;
    }

    .floating-shapes div:nth-child(1) {
        left: 10%;
        animation-duration: 28s;
        animation-delay: 0s;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(240, 147, 251, 0.3), transparent 70%);
    }

    .floating-shapes div:nth-child(2) {
        right: 5%;
        top: 20%;
        animation-duration: 32s;
        animation-delay: 5s;
        width: 250px;
        height: 250px;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.3), transparent 70%);
    }

    .floating-shapes div:nth-child(3) {
        bottom: 10%;
        left: 20%;
        animation-duration: 30s;
        animation-delay: 10s;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(118, 75, 162, 0.3), transparent 70%);
    }

    .floating-shapes div:nth-child(4) {
        top: 60%;
        right: 20%;
        animation-duration: 35s;
        animation-delay: 3s;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(255, 107, 107, 0.2), transparent 70%);
    }

    @keyframes floatShape {
        0% { transform: translateY(0) rotate(0deg) scale(1); }
        33% { transform: translateY(-30px) rotate(120deg) scale(1.1); }
        66% { transform: translateY(30px) rotate(240deg) scale(0.9); }
        100% { transform: translateY(0) rotate(360deg) scale(1); }
    }

    /* Стеклянные карточки с дополнительной тенью и прозрачностью */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border-radius: 32px;
        padding: 2rem 2.2rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.02);
        margin: 1.2rem 0;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        color: #fff;
    }

    .glass-card:hover {
        transform: translateY(-6px) scale(1.01);
        box-shadow: 0 35px 60px rgba(0, 0, 0, 0.4), 0 0 0 2px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.4);
    }

    /* Заголовок с неоновым свечением */
    .main-title {
        font-size: 4.8rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 30%, #4facfe 70%, #43e97b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 80px rgba(240, 147, 251, 0.3);
        letter-spacing: -3px;
        margin-bottom: 0.2rem;
        line-height: 1;
        animation: glowPulse 4s ease-in-out infinite;
    }

    @keyframes glowPulse {
        0%, 100% { text-shadow: 0 0 40px rgba(240, 147, 251, 0.2); }
        50% { text-shadow: 0 0 80px rgba(240, 147, 251, 0.5), 0 0 120px rgba(102, 126, 234, 0.2); }
    }

    .sub-title {
        text-align: center;
        font-size: 1.2rem;
        font-weight: 300;
        color: rgba(255, 255, 255, 0.6);
        letter-spacing: 6px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }

    /* Индикатор шагов */
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
        height: 2px;
        background: rgba(255, 255, 255, 0.1);
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
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: rgba(255,255,255,0.05);
        border: 2px solid rgba(255,255,255,0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: rgba(255,255,255,0.4);
        transition: all 0.4s ease;
        backdrop-filter: blur(8px);
        font-size: 1.1rem;
    }

    .step-circle.active {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        border-color: #f093fb;
        color: white;
        transform: scale(1.15);
        box-shadow: 0 8px 30px rgba(240, 147, 251, 0.4);
    }

    .step-circle.done {
        background: linear-gradient(135deg, #4facfe, #43e97b);
        border-color: #4facfe;
        color: white;
    }

    .step-label {
        margin-top: 8px;
        font-size: 0.75rem;
        font-weight: 600;
        color: rgba(255,255,255,0.4);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .step-label.active {
        color: #f093fb;
    }

    /* Поля ввода – прозрачные, с неоновой подсветкой */
    .stSelectbox > div, .stTextInput > div, .stFileUploader > div {
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        background: rgba(255,255,255,0.05) !important;
        backdrop-filter: blur(8px) !important;
        color: white !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }

    .stSelectbox > div:focus-within, .stTextInput > div:focus-within {
        border-color: #f093fb !important;
        box-shadow: 0 0 0 4px rgba(240, 147, 251, 0.15) !important;
        background: rgba(255,255,255,0.1) !important;
    }

    .stFileUploader > div {
        border: 2px dashed rgba(255,255,255,0.2) !important;
        background: rgba(255,255,255,0.03) !important;
        padding: 2rem !important;
        text-align: center;
    }

    .stFileUploader > div:hover {
        border-color: #f093fb !important;
        background: rgba(240, 147, 251, 0.05) !important;
    }

    /* Кнопка с неоновым градиентом и анимацией */
    .stButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border: none;
        color: white !important;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.8rem 2.5rem;
        border-radius: 60px;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 0 8px 30px rgba(240, 147, 251, 0.3);
        width: 100%;
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
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

    .stButton > button:hover {
        transform: scale(1.04) translateY(-3px);
        box-shadow: 0 15px 45px rgba(240, 147, 251, 0.5);
    }

    .stButton > button:hover::after {
        opacity: 1;
        transform: scale(1);
    }

    .stButton > button:active {
        transform: scale(0.96);
    }

    /* Карточки рекомендаций с градиентной рамкой */
    .rec-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.2rem;
        margin: 1rem 0;
    }

    .rec-card {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(8px);
        border-radius: 20px;
        padding: 1.2rem 1.5rem;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .rec-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(240,147,251,0.1), rgba(79,172,254,0.05));
        border-radius: 20px;
        z-index: -1;
    }

    .rec-card:hover {
        transform: translateY(-6px) scale(1.02);
        border-color: rgba(240,147,251,0.3);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }

    .rec-card h4 {
        font-size: 1rem;
        font-weight: 700;
        color: #fff;
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
        border-bottom: 1px solid rgba(255,255,255,0.05);
        font-weight: 400;
        color: rgba(255,255,255,0.8);
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .rec-card li:last-child {
        border-bottom: none;
    }

    .rec-card li::before {
        content: "✦";
        color: #f093fb;
        font-weight: 900;
        font-size: 0.8rem;
    }

    /* Цветовые квадраты */
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
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        border: 2px solid rgba(255,255,255,0.2);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .color-swatch:hover {
        transform: scale(1.15);
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
    }

    /* Совет стилиста – с градиентом и иконкой */
    .tip-box {
        background: linear-gradient(135deg, rgba(240,147,251,0.12), rgba(79,172,254,0.08));
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem 2rem;
        border: 1px solid rgba(255,255,255,0.06);
        margin: 1.5rem 0;
        font-style: italic;
        font-weight: 500;
        color: rgba(255,255,255,0.9);
        position: relative;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }

    .tip-box::before {
        content: "“";
        font-size: 3.5rem;
        color: rgba(240,147,251,0.3);
        position: absolute;
        top: -10px;
        left: 16px;
    }

    /* Теги параметров */
    .param-tag {
        display: inline-block;
        background: rgba(255,255,255,0.06);
        border-radius: 30px;
        padding: 0.2rem 1rem;
        font-size: 0.8rem;
        font-weight: 600;
        color: rgba(255,255,255,0.8);
        margin: 0.2rem 0.2rem;
        border: 1px solid rgba(255,255,255,0.08);
        transition: all 0.2s;
        backdrop-filter: blur(4px);
    }

    .param-tag:hover {
        background: rgba(240,147,251,0.2);
        color: #fff;
        border-color: rgba(240,147,251,0.4);
    }

    /* Сезонный бейдж */
    .season-badge {
        display: inline-block;
        padding: 0.4rem 1.2rem;
        border-radius: 40px;
        font-weight: 700;
        font-size: 0.9rem;
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        box-shadow: 0 4px 20px rgba(240, 147, 251, 0.3);
        text-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }

    /* Разделитель */
    .divider {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 2rem 0;
        color: rgba(255,255,255,0.2);
        font-size: 0.8rem;
        gap: 1rem;
    }

    .divider::before, .divider::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    }

    /* Анимация появления */
    .fade-in {
        animation: fadeInUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) both;
    }

    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(40px) scale(0.95); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }

    /* Подвал */
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.2);
        font-size: 0.75rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        letter-spacing: 1px;
    }

    /* Адаптив */
    @media (max-width: 640px) {
        .main-title { font-size: 2.8rem; }
        .glass-card { padding: 1.2rem; }
        .rec-grid { grid-template-columns: 1fr; }
        .step-progress { flex-direction: column; gap: 0.8rem; }
        .step-item { flex-direction: row; gap: 0.8rem; justify-content: flex-start; }
        .step-circle { width: 36px; height: 36px; font-size: 0.8rem; }
        .step-progress::before { display: none; }
    }
</style>
""", unsafe_allow_html=True)

# ------------------- ВСТАВЛЯЕМ ФОНОВЫЕ ЭЛЕМЕНТЫ -------------------
st.markdown("""
<div class="grid-overlay"></div>
<div class="floating-shapes">
    <div></div>
    <div></div>
    <div></div>
    <div></div>
</div>
""", unsafe_allow_html=True)

# ------------------- ЗАГОЛОВОК -------------------
st.markdown('<div class="main-title">StyleMate Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">✨ ИИ-стилист с премиум-анализом</div>', unsafe_allow_html=True)

# ------------------- ИНДИКАТОР ШАГОВ -------------------
step = 1
if "features" in st.session_state and st.session_state.get("auto_detected", False):
    step = 2
if "recommendations" in st.session_state:
    step = 3

st.markdown(f"""
<div class="step-progress">
    <div class="step-item">
        <div class="step-circle {'active' if step>=1 else ''}">1</div>
        <div class="step-label {'active' if step>=1 else ''}">Фото</div>
    </div>
    <div class="step-item">
        <div class="step-circle {'active' if step>=2 else ''}">2</div>
        <div class="step-label {'active' if step>=2 else ''}">Параметры</div>
    </div>
    <div class="step-item">
        <div class="step-circle {'active' if step>=3 else ''}">3</div>
        <div class="step-label {'active' if step>=3 else ''}">Образ</div>
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
            colors_html = "<div class='color-swatch-container'>"
            for color in rec["цвета"]:
                color_hex = {
                    "белый": "#FFFFFF", "черный": "#000000", "серый": "#808080",
                    "синий": "#4A90D9", "голубой": "#87CEEB", "лавандовый": "#B39DDB",
                    "розовый": "#FF6B81", "красный": "#FF4757", "бордовый": "#800020",
                    "зеленый": "#2ED573", "оливковый": "#808000", "мятный": "#98FF98",
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

    # Параметры в виде тегов
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
st.markdown('<div class="footer">© 2026 StyleMate Pro — создано с ❤️ для вашего стиля</div>', unsafe_allow_html=True)
