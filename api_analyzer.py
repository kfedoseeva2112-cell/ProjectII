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

# ------------------- ПРЕМИУМ CSS (светлый, с модными иконками) -------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css');

    * {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

    .stApp {
        background: transparent !important;
    }

    body::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: -2;
        background: linear-gradient(-45deg, #f8faff, #eef2ff, #fdf2f8, #f0f4ff);
        background-size: 400% 400%;
        animation: gradientBG 20s ease infinite;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    body::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: -1;
        background-image:
            radial-gradient(circle at 10% 20%, rgba(102, 126, 234, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 90% 80%, rgba(118, 75, 162, 0.12) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(240, 147, 251, 0.08) 0%, transparent 70%);
        background-repeat: no-repeat;
        animation: floatBubblesLight 18s ease-in-out infinite alternate;
    }

    @keyframes floatBubblesLight {
        0% { background-position: 10% 20%, 90% 80%, 50% 50%; }
        50% { background-position: 30% 40%, 70% 60%, 40% 70%; }
        100% { background-position: 50% 30%, 50% 90%, 60% 40%; }
    }

    .grid-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background-image:
            linear-gradient(rgba(0,0,0,0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,0,0,0.02) 1px, transparent 1px);
        background-size: 60px 60px;
        pointer-events: none;
    }

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
        opacity: 0.15;
        animation: floatShapeLight 25s linear infinite;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.2), transparent 70%);
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
        background: radial-gradient(circle, rgba(240, 147, 251, 0.15), transparent 70%);
    }

    .floating-shapes div:nth-child(2) {
        right: 5%;
        top: 20%;
        animation-duration: 32s;
        animation-delay: 5s;
        width: 250px;
        height: 250px;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.15), transparent 70%);
    }

    .floating-shapes div:nth-child(3) {
        bottom: 10%;
        left: 20%;
        animation-duration: 30s;
        animation-delay: 10s;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(118, 75, 162, 0.12), transparent 70%);
    }

    .floating-shapes div:nth-child(4) {
        top: 60%;
        right: 20%;
        animation-duration: 35s;
        animation-delay: 3s;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(255, 107, 107, 0.08), transparent 70%);
    }

    @keyframes floatShapeLight {
        0% { transform: translateY(0) rotate(0deg) scale(1); }
        33% { transform: translateY(-30px) rotate(120deg) scale(1.1); }
        66% { transform: translateY(30px) rotate(240deg) scale(0.9); }
        100% { transform: translateY(0) rotate(360deg) scale(1); }
    }

    /* Модные иконки на фоне */
    .fashion-icons {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        pointer-events: none;
        overflow: hidden;
        opacity: 0.12;
        font-size: 80px;
        color: rgba(102, 126, 234, 0.3);
    }

    .fashion-icons span {
        position: absolute;
        animation: floatIcon 30s linear infinite;
        display: block;
    }

    .fashion-icons span:nth-child(1) { top: 10%; left: 5%; animation-duration: 28s; animation-delay: 0s; font-size: 100px; }
    .fashion-icons span:nth-child(2) { top: 20%; right: 8%; animation-duration: 32s; animation-delay: 5s; font-size: 70px; }
    .fashion-icons span:nth-child(3) { bottom: 15%; left: 10%; animation-duration: 30s; animation-delay: 10s; font-size: 90px; }
    .fashion-icons span:nth-child(4) { bottom: 30%; right: 5%; animation-duration: 35s; animation-delay: 3s; font-size: 60px; }
    .fashion-icons span:nth-child(5) { top: 50%; left: 3%; animation-duration: 26s; animation-delay: 7s; font-size: 80px; }
    .fashion-icons span:nth-child(6) { top: 5%; left: 50%; animation-duration: 33s; animation-delay: 12s; font-size: 120px; }

    @keyframes floatIcon {
        0% { transform: translateY(0) rotate(0deg) scale(1); }
        33% { transform: translateY(-20px) rotate(120deg) scale(1.2); }
        66% { transform: translateY(20px) rotate(240deg) scale(0.8); }
        100% { transform: translateY(0) rotate(360deg) scale(1); }
    }

    /* Стеклянные карточки */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border-radius: 32px;
        padding: 2rem 2.2rem;
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.06), 0 0 0 1px rgba(0,0,0,0.01);
        margin: 1.2rem 0;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        color: #1a202c;
    }

    .glass-card:hover {
        transform: translateY(-6px) scale(1.01);
        box-shadow: 0 30px 60px rgba(102, 126, 234, 0.12);
        border-color: rgba(102, 126, 234, 0.2);
    }

    .main-title {
        font-size: 4.8rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 40%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 60px rgba(102, 126, 234, 0.15);
        letter-spacing: -3px;
        margin-bottom: 0.2rem;
        line-height: 1;
        animation: glowPulseLight 4s ease-in-out infinite;
    }

    @keyframes glowPulseLight {
        0%, 100% { text-shadow: 0 0 30px rgba(102, 126, 234, 0.1); }
        50% { text-shadow: 0 0 60px rgba(102, 126, 234, 0.25); }
    }

    .sub-title {
        text-align: center;
        font-size: 1.2rem;
        font-weight: 300;
        color: #6c7a9a;
        letter-spacing: 6px;
        border-bottom: 1px solid rgba(0,0,0,0.05);
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
    }

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
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: white;
        border: 2px solid #cbd5e0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: #4a5568;
        transition: all 0.4s ease;
        font-size: 1.1rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.02);
    }

    .step-circle.active {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-color: #667eea;
        color: white;
        transform: scale(1.15);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.25);
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

    .stSelectbox > div, .stTextInput > div, .stFileUploader > div {
        border-radius: 16px !important;
        border: 2px solid #e2e8f0 !important;
        background: rgba(255,255,255,0.6) !important;
        backdrop-filter: blur(4px) !important;
        color: #1a202c !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
    }

    .stSelectbox > div:focus-within, .stTextInput > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1) !important;
        background: white !important;
    }

    .stFileUploader > div {
        border: 2px dashed #cbd5e0 !important;
        background: rgba(247, 250, 252, 0.5) !important;
        padding: 2rem !important;
        text-align: center;
    }

    .stFileUploader > div:hover {
        border-color: #667eea !important;
        background: rgba(102, 126, 234, 0.03) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border: none;
        color: white !important;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.8rem 2.5rem;
        border-radius: 60px;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.25);
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
        box-shadow: 0 15px 45px rgba(102, 126, 234, 0.35);
    }

    .stButton > button:hover::after {
        opacity: 1;
        transform: scale(1);
    }

    .stButton > button:active {
        transform: scale(0.96);
    }

    .rec-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.2rem;
        margin: 1rem 0;
    }

    .rec-card {
        background: rgba(255,255,255,0.6);
        backdrop-filter: blur(8px);
        border-radius: 20px;
        padding: 1.2rem 1.5rem;
        border: 1px solid rgba(255,255,255,0.8);
        box-shadow: 0 8px 24px rgba(0,0,0,0.04);
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
        background: linear-gradient(135deg, rgba(102,126,234,0.05), rgba(240,147,251,0.03));
        border-radius: 20px;
        z-index: -1;
    }

    .rec-card:hover {
        transform: translateY(-6px) scale(1.02);
        border-color: rgba(102,126,234,0.2);
        box-shadow: 0 20px 40px rgba(0,0,0,0.06);
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
        content: "✦";
        color: #667eea;
        font-weight: 900;
        font-size: 0.8rem;
    }

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
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        border: 2px solid white;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .color-swatch:hover {
        transform: scale(1.15);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }

    .tip-box {
        background: rgba(250, 245, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem 2rem;
        border: 1px solid rgba(102,126,234,0.1);
        margin: 1.5rem 0;
        font-style: italic;
        font-weight: 500;
        color: #2d3748;
        position: relative;
        box-shadow: 0 4px 20px rgba(0,0,0,0.02);
    }

    .tip-box::before {
        content: "“";
        font-size: 3.5rem;
        color: rgba(102,126,234,0.15);
        position: absolute;
        top: -10px;
        left: 16px;
    }

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

    .season-badge {
        display: inline-block;
        padding: 0.4rem 1.2rem;
        border-radius: 40px;
        font-weight: 700;
        font-size: 0.9rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 4px 20px rgba(102,126,234,0.2);
    }

    .divider {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 2rem 0;
        color: #cbd5e0;
        font-size: 0.8rem;
        gap: 1rem;
    }

    .divider::before, .divider::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, transparent, #cbd5e0, transparent);
    }

    .fade-in {
        animation: fadeInUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) both;
    }

    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(40px) scale(0.95); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }

    .footer {
        text-align: center;
        color: #a0aec0;
        font-size: 0.75rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #edf2f7;
        letter-spacing: 1px;
    }

    @media (max-width: 640px) {
        .main-title { font-size: 2.8rem; }
        .glass-card { padding: 1.2rem; }
        .rec-grid { grid-template-columns: 1fr; }
        .step-progress { flex-direction: column; gap: 0.8rem; }
        .step-item { flex-direction: row; gap: 0.8rem; justify-content: flex-start; }
        .step-circle { width: 36px; height: 36px; font-size: 0.8rem; }
        .step-progress::before { display: none; }
        .fashion-icons { opacity: 0.06; }
    }
</style>
""", unsafe_allow_html=True)

# ------------------- ФОНОВЫЕ ЭЛЕМЕНТЫ -------------------
st.markdown("""
<div class="grid-overlay"></div>
<div class="floating-shapes">
    <div></div>
    <div></div>
    <div></div>
    <div></div>
</div>
<div class="fashion-icons">
    <span>💄</span>
    <span>👗</span>
    <span>👠</span>
    <span>🧥</span>
    <span>👜</span>
    <span>✂️</span>
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

# Если фото загружено
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ваше фото", use_column_width=True)

    current_file_name = uploaded_file.name

    # Проверяем, были ли уже распознаны параметры для этого фото
    if "features" in st.session_state and st.session_state.get("last_file_name") == current_file_name:
        st.success("✅ Параметры уже распознаны для этого фото (использованы сохранённые данные).")
        features = st.session_state.features
        # Показываем распознанные параметры (красиво)
        st.markdown("**Распознанные параметры:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"- **Пол:** {gender_map.get(features.get('gender', 'неизвестно'), 'неизвестно')}")
            st.markdown(f"- **Тон кожи:** {skin_map.get(features.get('skin_tone', 'неизвестно'), 'неизвестно')}")
            st.markdown(f"- **Цвет волос:** {hair_map.get(features.get('hair_color', 'неизвестно'), 'неизвестно')}")
        with col2:
            st.markdown(f"- **Возраст:** {age_map.get(features.get('age_category', 'неизвестно'), 'неизвестно')}")
            st.markdown(f"- **Цвет глаз:** {eyes_map.get(features.get('eye_color', 'неизвестно'), 'неизвестно')}")
            st.markdown(f"- **Раса:** {race_map.get(features.get('race', 'неизвестно'), 'неизвестно')}")
    else:
        # Кнопка для распознавания
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
                    st.session_state.last_file_name = current_file_name  # запоминаем
                    st.rerun()
else:
    # Если фото не загружено – сбрасываем сохранённое имя, чтобы при новом фото всё переопределялось
    if "last_file_name" in st.session_state:
        del st.session_state.last_file_name
    # features можно оставить, но они не будут использоваться

st.markdown('</div>', unsafe_allow_html=True)

# ------------------- ШАГ 2: ПАРАМЕТРЫ -------------------
st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
st.markdown("#### ✏️ Шаг 2. Уточните все параметры внешности")
st.markdown("_Чем точнее вы заполните, тем лучше будет результат._")

# Значения по умолчанию – если есть распознанные, подставляем их
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

# ------------------- ВЫВОД РЕЗУЛЬТАТА (или заглушки) -------------------
if "recommendations" in st.session_state:
    rec = st.session_state.recommendations
    features_full = st.session_state.features_full

    st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
    st.markdown("#### 🌟 Ваш персональный образ готов!")

    season_emoji = {"spring": "🌸", "summer": "☀️", "autumn": "🍂", "winter": "❄️"}
    st.markdown(f"<div style='display:flex; gap:10px; flex-wrap:wrap; margin-bottom:1rem;'>"
                f"<span class='season-badge'>{season_emoji.get(features_full['color_type'], '')} {color_type_map.get(features_full['color_type'], '')}</span>"
                f"</div>", unsafe_allow_html=True)

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

    if rec.get("style_tip"):
        st.markdown(f"""
        <div class="tip-box">
            <strong>💡 Совет стилиста:</strong> {rec['style_tip']}
        </div>
        """, unsafe_allow_html=True)

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

else:
    # Заглушки: показываем стильные советы
    st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
    st.markdown("#### 💡 Ваш будущий образ")
    st.markdown("_Заполните параметры и нажмите «Создать идеальный образ», чтобы получить персональные рекомендации._")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="rec-card" style="border-left-color: #f6ad55;">
            <h4>👗 Совет дня</h4>
            <ul>
                <li>Носите то, что подчеркивает вашу индивидуальность</li>
                <li>Качественные базовые вещи – основа гардероба</li>
                <li>Одна яркая деталь может преобразить всё</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="rec-card" style="border-left-color: #4facfe;">
            <h4>🎨 Цветовая гармония</h4>
            <ul>
                <li>Подбирайте оттенки под свой цветотип</li>
                <li>Контрастные акценты делают образ ярче</li>
                <li>Используйте правило 60-30-10</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="rec-card" style="border-left-color: #43e97b;">
            <h4>💡 Аксессуары</h4>
            <ul>
                <li>Один яркий аксессуар – и образ заиграет</li>
                <li>Следуйте правилу «меньше – значит больше»</li>
                <li>Учитывайте форму лица при выборе серёг</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------- ПОДВАЛ -------------------
st.markdown("---")
with st.expander("ℹ️ Как это работает"):
    st.markdown("""
    **StyleMate Pro** использует передовые алгоритмы компьютерного зрения и стилистические правила.
    Вы загружаете фото, система определяет параметры внешности, а затем на основе ваших данных и выбранного мероприятия подбирает идеальный образ.

    **Технологии:**
    - Распознавание лиц: Face++ API (реальное)
    - База стилистических правил: более 40 комбинаций
    - Интерфейс: Streamlit с кастомным CSS
    """)
st.markdown('<div class="footer">© 2026 StyleMate Pro — создано с ❤️ для вашего стиля</div>', unsafe_allow_html=True)
