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

# ------------------- CSS (премиум-светлый, полный) -------------------
st.markdown("""
<style>
    /* Ваш существующий CSS (я сократил для экономии места, вставьте свой полный CSS) */
    /* ... (полный CSS из предыдущих версий) ... */
</style>
""", unsafe_allow_html=True)

# ------------------- ФОНОВЫЕ ЭЛЕМЕНТЫ -------------------
st.markdown("""
<div class="fashion-icons">
    <span>💄</span>
    <span>👗</span>
    <span>👠</span>
    <span>🧥</span>
    <span>👜</span>
    <span>✂️</span>
</div>
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
if "recommendations" in st.session_state and st.session_state.recommendations is not None:
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

# ------------------- ИНИЦИАЛИЗАЦИЯ СЕССИИ -------------------
if "features" not in st.session_state:
    st.session_state.features = {}
if "auto_detected" not in st.session_state:
    st.session_state.auto_detected = False
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None
if "features_full" not in st.session_state:
    st.session_state.features_full = {}
if "last_uploaded_name" not in st.session_state:
    st.session_state.last_uploaded_name = None
# Словарь для сохранения параметров по имени файла
if "saved_features" not in st.session_state:
    st.session_state.saved_features = {}

# ------------------- ЗАГРУЗКА ФОТО -------------------
st.markdown("#### 📸 Шаг 1. Загрузите ваше фото")
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed", key="photo_uploader")

# --- ОБРАБОТКА ЗАГРУЗКИ ФОТО ---
if uploaded_file is not None:
    current_name = uploaded_file.name
    # Проверяем, есть ли сохранённые параметры для этого файла
    if current_name in st.session_state.saved_features:
        # Загружаем сохранённые параметры
        st.session_state.features = st.session_state.saved_features[current_name]
        st.session_state.auto_detected = True
        st.session_state.last_uploaded_name = current_name
        # Не сбрасываем рекомендации, если они уже были для этого файла
        # (можно дополнительно сохранять рекомендации, но пока оставим так)
    else:
        # Новый файл – сбрасываем только если имя изменилось (защита от повторной загрузки)
        if st.session_state.last_uploaded_name != current_name:
            st.session_state.features = {}
            st.session_state.auto_detected = False
            st.session_state.recommendations = None
            st.session_state.features_full = {}
            st.session_state.last_uploaded_name = current_name
            st.rerun()

    # Отображаем фото
    image = Image.open(uploaded_file)
    st.image(image, caption="Ваше фото", use_column_width=True)

    # Кнопка распознавания
    if st.button("🔍 Распознать параметры по фото", type="primary"):
        with st.spinner("Анализируем фото..."):
            bytes_data = uploaded_file.getvalue()
            features = analyze_face(bytes_data)
            if "error" in features:
                st.error(f"❌ {features['error']}")
                st.session_state.features = {}
                st.session_state.auto_detected = False
            else:
                st.success("✅ Параметры распознаны!")
                st.session_state.features = features
                st.session_state.auto_detected = True
                # Сохраняем для этого файла
                st.session_state.saved_features[current_name] = features
                st.rerun()
else:
    # Если файл удалён – ничего не сбрасываем, но можно очистить last_uploaded_name
    if st.session_state.last_uploaded_name is not None:
        st.session_state.last_uploaded_name = None

# ------------------- РУЧНОЙ ВВОД ПАРАМЕТРОВ -------------------
st.markdown("#### ✏️ Шаг 2. Уточните параметры внешности")
st.markdown("_Чем точнее вы заполните, тем лучше будет результат._")

# Значения по умолчанию – из сохранённых (если есть) или стандартные
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

# ------------------- КНОПКА ПОДБОРА И СОХРАНЕНИЕ ПАРАМЕТРОВ -------------------
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
    # Сохраняем текущие параметры для текущего файла (если он загружен)
    if uploaded_file is not None:
        current_name = uploaded_file.name
        # Обновляем сохранённые параметры (включая ручные правки)
        st.session_state.saved_features[current_name] = features_full
    st.rerun()

# ------------------- ВЫВОД РЕЗУЛЬТАТА -------------------
if st.session_state.recommendations is not None and uploaded_file is not None:
    rec = st.session_state.recommendations
    features_full = st.session_state.features_full

    st.markdown("#### 🌟 Ваш персональный образ готов!")

    # Бейдж цветотипа
    if "color_type" in features_full:
        season_emoji = {"spring": "🌸", "summer": "☀️", "autumn": "🍂", "winter": "❄️"}
        st.markdown(f"""
        <div style='display:flex; gap:10px; flex-wrap:wrap; margin-bottom:1rem;'>
            <span class='season-badge'>{season_emoji.get(features_full['color_type'], '')} {color_type_map.get(features_full['color_type'], '')}</span>
        </div>
        """, unsafe_allow_html=True)

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
            color_hex_map = {
                "белый": "#FFFFFF", "черный": "#000000", "серый": "#808080",
                "синий": "#4A90D9", "голубой": "#87CEEB", "лавандовый": "#B39DDB",
                "розовый": "#FF6B81", "красный": "#FF4757", "бордовый": "#800020",
                "зеленый": "#2ED573", "оливковый": "#808000", "мятный": "#98FF98",
                "желтый": "#FFC107", "золотой": "#FFD700", "бежевый": "#F5F5DC",
                "оранжевый": "#FD7E14", "персиковый": "#FFDAB9", "терракотовый": "#CC7A4B",
                "вишневый": "#800020", "изумрудный": "#50C878", "бирюзовый": "#40E0D0",
                "фиолетовый": "#8A2BE2", "сиреневый": "#C8A2C8", "серебро": "#C0C0C0"
            }
            colors_html = "<div class='color-swatch-container'>"
            for color in rec["цвета"]:
                hex_color = color_hex_map.get(color.lower(), "#6C63FF")
                colors_html += f"<div class='color-swatch' style='background:{hex_color};'></div>"
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

# ------------------- ЗАГЛУШКИ (если рекомендаций ещё нет) -------------------
else:
    st.markdown("#### 💡 Ваш будущий образ")
    st.markdown("_Заполните параметры и нажмите «Создать идеальный образ»._")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="rec-card" style="border-left-color: #f6ad55;">
            <h4>👗 Совет дня</h4>
            <ul>
                <li>Носите то, что подчеркивает индивидуальность</li>
                <li>Качественные базовые вещи – основа гардероба</li>
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
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="rec-card" style="border-left-color: #43e97b;">
            <h4>💡 Аксессуары</h4>
            <ul>
                <li>Один яркий аксессуар – и образ заиграет</li>
                <li>Меньше – значит больше</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ------------------- ПОДВАЛ -------------------
st.markdown("---")
with st.expander("ℹ️ Как это работает"):
    st.markdown("""
    **StyleMate Pro** анализирует фото, определяет тон кожи и подбирает детерминированные параметры.
    Вы можете скорректировать их вручную, выбрать мероприятие и получить персонализированные рекомендации.
    """)
st.markdown('<div class="footer">© 2026 StyleMate Pro — создано с ❤️</div>', unsafe_allow_html=True)
