if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ваше фото", use_column_width=True)
    
    if st.button("🔍 Распознать параметры по фото", type="primary"):
        with st.spinner("Анализируем лицо..."):
            bytes_data = uploaded_file.getvalue()
            features = analyze_face(bytes_data)
            if "error" in features:
                st.error(f"❌ {features['error']}")
            else:
                st.success("✅ Параметры распознаны!")
                st.session_state.features = features
                st.session_state.auto_detected = True
                
                # Красивый вывод параметров
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Пол:** {gender_map.get(features.get('gender'), 'неизвестно')}")
                    st.markdown(f"**Тон кожи:** {skin_map.get(features.get('skin_tone'), 'неизвестно')}")
                    st.markdown(f"**Цвет волос:** {hair_map.get(features.get('hair_color'), 'неизвестно')}")
                with col2:
                    st.markdown(f"**Возраст:** {age_map.get(features.get('age_category'), 'неизвестно')}")
                    st.markdown(f"**Цвет глаз:** {eyes_map.get(features.get('eye_color'), 'неизвестно')}")
                    st.markdown(f"**Раса:** {race_map.get(features.get('race'), 'неизвестно')}")
                
                # Автоматический подбор
                occasion = st.session_state.get("occasion", "Офис")
                recommendations = get_recommendations(features, occasion)
                # ... вывод рекомендаций (как в коде выше)
