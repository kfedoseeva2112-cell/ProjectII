import streamlit as st
from PIL import Image
from api_analyzer import analyze_face
from matcher import get_recommendations

# --- Настройка страницы ---
st.set_page_config(page_title="StyleMate", layout="centered", initial_sidebar_state="collapsed")

# --- ПРЕМИУМ CSS (дизайн от профи) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6C63FF, #FF6B6B, #FECA57);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }
    .sub-title {
        text-align: center;
        color: #6C757D;
        font-size: 1.2rem;
        font-weight: 300;
        margin-bottom: 2rem;
        letter-spacing: 2px;
    }
    .rec-card {
        background: white;
        border-radius: 20px;
        padding: 25px 30px;
        margin: 15px 0;
        box-shadow: 0 10px 40px rgba(108, 99, 255, 0.1);
        border-left: 5px solid #6C63FF;
        transition: transform 0.2s;
    }
    .rec-card:hover { transform: translateY(-3px); }
    .stButton > button {
        background: linear-gradient(135deg, #6C63FF, #5A52D5);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 12px 40px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s;
        box-shadow: 0 5px 20px rgba(108, 99, 255, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(108, 99, 255, 0.4);
    }
    .divider {
        background: linear-gradient(90deg, transparent, #6C63FF, transparent);
        height: 2px;
        margin: 30px 0;
        opacity: 0.3;
    }
    .tip-box {
        background: #F8F9FA;
        border-radius: 16px;
        padding: 20px 25px;
        border: 1px solid #E9ECEF;
    }
</style>
""", unsafe_allow_html=True)

# --- Заголовки ---
st.markdown('<div class="main-title">StyleMate</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Ваш персональный AI-стилист</div>', unsafe_allow_html=True)

# --- Загрузка фото ---
uploaded_file = st.file_uploader("📸 Загрузите ваше фото", type=["jpg", "jpeg", "png"])

col1, col2 = st.columns([1, 2])
with col1:
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Ваше фото", use_column_width=True)

with col2:
    if uploaded_file is not None:
        if st.button("🔍 Распознать параметры по фото", type="primary"):
            with st.spinner("Анализируем лицо (это может занять 10–15 секунд)..."):
                bytes_data = uploaded_file.getvalue()
                features = analyze_face(bytes_data)
                if "error" in features:
                    st.error(f"❌ {features['error']}")
                    st.info("Пожалуйста, введите параметры вручную ниже.")
                else:
                   st.success("✅ Параметры распознаны! Нажмите кнопку ниже, чтобы получить образ.")
st.session_state.features = features
st.session_state.auto_detected = True

# Показываем распознанные параметры красиво (без JSON)
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Пол:** {gender_map.get(features.get('gender', 'неизвестно'), 'неизвестно')}")
    st.markdown(f"**Тон кожи:** {skin_map.get(features.get('skin_tone', 'неизвестно'), 'неизвестно')}")
    st.markdown(f"**Цвет волос:** {hair_map.get(features.get('hair_color', 'неизвестно'), 'неизвестно')}")
with col2:
    st.markdown(f"**Возраст:** {age_map.get(features.get('age_category', 'неизвестно'), 'неизвестно')}")
    st.markdown(f"**Цвет глаз:** {eyes_map.get(features.get('eye_color', 'неизвестно'), 'неизвестно')}")
    st.markdown(f"**Раса:** {race_map.get(features.get('race', 'неизвестно'), 'неизвестно')}")
# --- Ручной ввод (всегда доступен) ---
st.markdown("---")
st.subheader("✏️ Параметры внешности (введите сами, если автоматика не сработала)")

# Подставляем распознанные значения, если есть
default_gender = st.session_state.get("features", {}).get("gender", "female")
default_skin = st.session_state.get("features", {}).get("skin_tone", "fair")
default_hair = st.session_state.get("features", {}).get("hair_color", "blond")
default_eyes = st.session_state.get("features", {}).get("eye_color", "blue")
default_race = st.session_state.get("features", {}).get("race", "caucasian")
default_age = st.session_state.get("features", {}).get("age_category", "young")

# Маппинг для отображения на русском
gender_map = {"female": "Женский", "male": "Мужской"}
skin_map = {"fair": "Светлая", "medium": "Средняя", "dark": "Тёмная"}
hair_map = {"blond": "Блондин", "brown": "Шатен", "black": "Брюнет", "red": "Рыжий", "gray": "Седой"}
eyes_map = {"blue": "Голубые", "green": "Зелёные", "brown": "Карие", "hazel": "Ореховые"}
race_map = {"caucasian": "Европеец", "asian": "Азиат", "african": "Африканец", "hispanic": "Латиноамериканец"}
age_map = {"young": "Молодой", "middle": "Средний", "old": "Зрелый"}

col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Пол", options=list(gender_map.keys()), format_func=lambda x: gender_map[x], index=list(gender_map.keys()).index(default_gender) if default_gender in gender_map else 0)
    skin_tone = st.selectbox("Тон кожи", options=list(skin_map.keys()), format_func=lambda x: skin_map[x], index=list(skin_map.keys()).index(default_skin) if default_skin in skin_map else 0)
    hair_color = st.selectbox("Цвет волос", options=list(hair_map.keys()), format_func=lambda x: hair_map[x], index=list(hair_map.keys()).index(default_hair) if default_hair in hair_map else 0)
with col2:
    age_category = st.selectbox("Возрастная категория", options=list(age_map.keys()), format_func=lambda x: age_map[x], index=list(age_map.keys()).index(default_age) if default_age in age_map else 0)
    eye_color = st.selectbox("Цвет глаз", options=list(eyes_map.keys()), format_func=lambda x: eyes_map[x], index=list(eyes_map.keys()).index(default_eyes) if default_eyes in eyes_map else 0)
    race = st.selectbox("Раса", options=list(race_map.keys()), format_func=lambda x: race_map[x], index=list(race_map.keys()).index(default_race) if default_race in race_map else 0)

# --- ВЫБОР МЕРОПРИЯТИЯ (новое!) ---
st.subheader("📅 Для какого случая подбираем образ?")
occasion = st.selectbox(
    "Выберите мероприятие",
    options=["Офис", "Свидание", "Вечеринка", "Прогулка", "Спорт", "Деловая встреча", "Свадьба", "Отдых"],
    index=0
)

# --- Кнопка подбора ---
# --- БЛОК АВТОМАТИЧЕСКОГО ПОДБОРА ПОСЛЕ РАСПОЗНАВАНИЯ ---
# Если в сессии есть распознанные параметры и флаг auto_detected = True
if "features" in st.session_state and st.session_state.get("auto_detected", False):
    features_manual = st.session_state.features
    # Берём мероприятие из сессии (если не выбрано, то "Офис")
    occasion = st.session_state.get("occasion", "Офис")
    
    recommendations = get_recommendations(features_manual, occasion)
    
    st.markdown("---")
    st.subheader("🌟 Ваш персональный образ")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**👗 Одежда**")
        for item in recommendations.get("одежда", []):
            st.markdown(f"- {item}")
        st.markdown("**🎨 Цветовая палитра**")
        for color in recommendations.get("цвета", []):
            st.markdown(f"- {color}")
    with col2:
        st.markdown("**💍 Аксессуары**")
        for acc in recommendations.get("аксессуары", []):
            st.markdown(f"- {acc}")
        st.markdown("**💄 Макияж**")
        for m in recommendations.get("makeup", []):
            st.markdown(f"- {m}")
    
    st.info(f"💡 **Совет стилиста:** {recommendations.get('style_tip', '')}")
    
    # Сбрасываем флаг, чтобы не дублировать при повторных обновлениях
    st.session_state.auto_detected = False

# --- КНОПКА ДЛЯ РУЧНОГО ПОДБОРА (всегда доступна) ---
if st.button("✨ Подобрать образ вручную (по выбранным параметрам)", type="secondary", use_container_width=True):
    features_manual = {
        "gender": gender,
        "skin_tone": skin_tone,
        "hair_color": hair_color,
        "eye_color": eye_color,
        "race": race,
        "age_category": age_category
    }
    recommendations = get_recommendations(features_manual, occasion)
    
    st.markdown("---")
    st.subheader("🌟 Ваш персональный образ")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**👗 Одежда**")
        for item in recommendations.get("одежда", []):
            st.markdown(f"- {item}")
        st.markdown("**🎨 Цветовая палитра**")
        for color in recommendations.get("цвета", []):
            st.markdown(f"- {color}")
    with col2:
        st.markdown("**💍 Аксессуары**")
        for acc in recommendations.get("аксессуары", []):
            st.markdown(f"- {acc}")
        st.markdown("**💄 Макияж**")
        for m in recommendations.get("makeup", []):
            st.markdown(f"- {m}")
    
    st.info(f"💡 **Совет стилиста:** {recommendations.get('style_tip', '')}")

# --- Подвал ---
st.markdown("---")
with st.expander("ℹ️ Как это работает"):
    st.markdown("""
    **StyleMate** анализирует ваше фото через локальную нейросеть (DeepFace) и определяет пол, возраст и расу.
    Вы также можете ввести параметры вручную. На основе выбранного мероприятия и стилистических правил мы подбираем идеальный образ.
    """)
