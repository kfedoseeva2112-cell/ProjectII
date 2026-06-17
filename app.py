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

# ------------------- CSS (ваш премиум-стиль) -------------------
st.markdown("""
<style>
    /* Ваш CSS код (я сократил для читаемости, вставьте свой полный блок) */
    ... (ваш существующий CSS) ...
</style>
""", unsafe_allow_html=True)

# ------------------- ЗАГОЛОВОК -------------------
st.markdown('<div class="main-title">StyleMate Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">✨ ИИ-стилист с премиум-анализом</div>', unsafe_allow_html=True)

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

# ------------------- ЗАГРУЗКА ФОТО -------------------
st.markdown("#### 📸 Шаг 1. Загрузите ваше фото")
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

# --- ЕСЛИ ЗАГРУЖЕНО НОВОЕ ФОТО, СБРАСЫВАЕМ СТАРЫЕ ПАРАМЕТРЫ ---
if uploaded_file is not None:
    # Проверяем, изменился ли файл (по имени или содержимому)
    # Просто сбрасываем features при каждом новом файле
    if "prev_file" not in st.session_state or st.session_state.prev_file != uploaded_file.name:
        st.session_state.features = {}
        st.session_state.auto_detected = False
        st.session_state.prev_file = uploaded_file.name
        st.rerun()  # перерисовываем страницу, чтобы поля обновились

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
                # Если ошибка, очищаем сессию
                st.session_state.features = {}
                st.session_state.auto_detected = False
            else:
                st.success("✅ Параметры распознаны!")
                st.session_state.features = features
                st.session_state.auto_detected = True
                st.rerun()  # <-- ОБНОВЛЯЕМ ИНТЕРФЕЙС С НОВЫМИ ПАРАМЕТРАМИ

# ------------------- РУЧНОЙ ВВОД ПАРАМЕТРОВ -------------------
st.markdown("#### ✏️ Шаг 2. Уточните параметры внешности")
st.markdown("_Чем точнее вы заполните, тем лучше будет результат._")

# Если есть распознанные параметры, используем их как default
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

# ------------------- ВЫБОР МЕРОПРИЯТИЯ -------------------
st.markdown("#### 📅 Шаг 3. Выберите случай")
occasion = st.selectbox(
    "Для какого мероприятия подбираем образ?",
    options=["Офис", "Свидание", "Вечеринка", "Прогулка", "Спорт", "Деловая встреча", "Свадьба", "Отдых"],
    index=0,
    key="occasion_select"
)
st.session_state.occasion = occasion

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

# ------------------- ВЫВОД РЕЗУЛЬТАТА (рекомендации или заглушки) -------------------
if "recommendations" in st.session_state:
    rec = st.session_state.recommendations
    features_full = st.session_state.features_full

    st.markdown("#### 🌟 Ваш персональный образ готов!")
    # ... ваш код вывода рекомендаций (оставьте как есть) ...
else:
    st.markdown("#### 💡 Ваш будущий образ")
    st.markdown("_Заполните параметры и нажмите «Создать идеальный образ»._")
    # ... ваши карточки-заглушки ...

# ------------------- ПОДВАЛ -------------------
st.markdown("---")
with st.expander("ℹ️ Как это работает"):
    st.markdown("""
    **StyleMate Pro** использует анализ цвета и детерминированный алгоритм для определения параметров.
    Вы можете загрузить фото и нажать «Распознать», чтобы заполнить поля автоматически.
    Затем выберите мероприятие и получите персональные рекомендации.
    """)
st.markdown('<div class="footer">© 2026 StyleMate Pro</div>', unsafe_allow_html=True)
