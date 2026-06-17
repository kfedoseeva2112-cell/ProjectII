import streamlit as st
from PIL import Image
from api_analyzer import analyze_face
from matcher import get_recommendations

st.set_page_config(page_title="StyleMate", layout="centered", initial_sidebar_state="collapsed")

# --- Стилизация ---
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .feature-box {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .recommendation {
        background: #fff;
        border-left: 5px solid #4ecdc4;
        padding: 15px 20px;
        margin: 10px 0;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎨 StyleMate</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Интеллектуальный стилист на основе компьютерного зрения</div>', unsafe_allow_html=True)

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
            with st.spinner("Анализируем лицо..."):
                bytes_data = uploaded_file.getvalue()
                features = analyze_face(bytes_data)
                if "error" in features:
                    st.error(f"❌ {features['error']}")
                    st.info("Пожалуйста, введите параметры вручную ниже.")
                else:
                    st.success("✅ Параметры распознаны!")
                    # Сохраняем в session_state
                    st.session_state.features = features
                    st.session_state.auto_detected = True
                    # Показываем что распознано
                    st.json(features)

# --- Ручной ввод параметров (всегда доступен) ---
st.markdown("---")
st.subheader("✏️ Параметры внешности (введите вручную, если автоматика не сработала)")

# Если есть распознанные параметры, подставляем их как значения по умолчанию
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

# --- Кнопка подбора ---
if st.button("✨ Подобрать идеальный образ!", type="primary", use_container_width=True):
    features_manual = {
        "gender": gender,
        "skin_tone": skin_tone,
        "hair_color": hair_color,
        "eye_color": eye_color,
        "race": race,
        "age_category": age_category
    }
    recommendations = get_recommendations(features_manual)

    st.markdown("---")
    st.subheader("🌟 Ваш персональный образ")

    # Вывод в две колонки
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

# --- Блок с описанием (для красоты) ---
st.markdown("---")
with st.expander("ℹ️ Как это работает"):
    st.markdown("""
    **StyleMate** использует передовые алгоритмы компьютерного зрения для анализа вашей внешности.
    Вы можете загрузить фото и нажать «Распознать параметры», либо ввести их вручную.
    На основе ваших параметров и базы стилистических правил мы подбираем идеальный образ.
    """)
