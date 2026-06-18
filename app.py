import streamlit as st
from PIL import Image
from api_analyzer import analyze_face
from matcher import get_recommendationsst.markdown("#### 💄 Макияж")
makeup_list = rec.get("makeup")
if makeup_list and len(makeup_list) > 0:
    st.markdown(f"""
    <div class="rec-card">
        <ul>
            {''.join([f'<li>{item}</li>' for item in makeup_list])}
        </ul>
    </div>
    """, unsafe_allow_html=True)
else:
    # Если нет макияжа – показываем дефолтный
    st.markdown("""
    <div class="rec-card">
        <ul>
            <li>Естественный макияж</li>
            <li>Лёгкий тональный крем</li>
            <li>Помада нюдового оттенка</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
