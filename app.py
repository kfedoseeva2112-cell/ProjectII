from PIL import Image
import streamlit as st
from matcher import get_recommendations

st.set_page_config(page_title="StyleMate AI", layout="centered")
st.title("🎨 StyleMate — ваш интеллектуальный стилист")
st.markdown("Загрузите фото и укажите параметры внешности для персонализированного подбора.")

# Загрузка фото (только для красоты)
uploaded_file = st.file_uploader("Загрузите ваше фото", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ваше фото", use_column_width=True)

# Ручной ввод параметров
st.subheader("Параметры внешности")
col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Пол", ["female", "male"])
    skin_tone = st.selectbox("Тон кожи", ["fair", "medium", "dark"])
    hair_color = st.selectbox("Цвет волос", ["blond", "brown", "black", "red", "gray"])
with col2:
    age_category = st.selectbox("Возрастная категория", ["young", "middle", "old"])
    eye_color = st.selectbox("Цвет глаз", ["blue", "green", "brown", "hazel"])
    race = st.selectbox("Раса", ["caucasian", "asian", "african", "hispanic"])

if st.button("Подобрать образ!"):
    features = {
        "gender": gender,
        "skin_tone": skin_tone,
        "hair_color": hair_color,
        "eye_color": eye_color,
        "race": race,
        "age_category": age_category
    }
    recommendations = get_recommendations(features)
    
    st.subheader("✨ Ваш персональный образ")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Одежда:**")
        for item in recommendations.get("одежда", []):
            st.write(f"- {item}")
        st.markdown("**Цветовая палитра:**")
        for color in recommendations.get("цвета", []):
            st.write(f"- {color}")
    with col2:
        st.markdown("**Аксессуары:**")
        for acc in recommendations.get("аксессуары", []):
            st.write(f"- {acc}")
        st.markdown("**Макияж:**")
        for m in recommendations.get("makeup", []):
            st.write(f"- {m}")
    st.info(f"💡 Совет стилиста: {recommendations.get('style_tip', '')}")
