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
