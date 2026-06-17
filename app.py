import streamlit as st
import requests
from PIL import Image
import io
from api_analyzer import analyze_face
from matcher import get_recommendations

st.set_page_config(page_title="StyleMate AI", layout="centered")
st.title("🎨 StyleMate — ваш интеллектуальный стилист")
st.markdown("Загрузите своё фото, и ИИ подберёт идеальный образ.")

uploaded_file = st.file_uploader("Выберите фото", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Показываем фото
    image = Image.open(uploaded_file)
    st.image(image, caption="Ваше фото", use_column_width=True)
    
    with st.spinner("Анализируем внешность с помощью ИИ..."):
        # Читаем байты
        bytes_data = uploaded_file.getvalue()
        # Вызываем API-анализ
        features = analyze_face(bytes_data)
    
    if "error" in features:
        st.error(features["error"])
    else:
        st.success("Анализ завершён!")
        # Показываем, что определили (для наглядности)
        st.write("Определённые параметры:", features)
        
        # Передаём параметры в matcher
        recommendations = get_recommendations(features)
        
        # Выводим результат
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
