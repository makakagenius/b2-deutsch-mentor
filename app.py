import streamlit as st
import google.generativeai as genai

# 1. Настройка страницы (строго в самом начале!)
st.set_page_config(
    page_title="B2 Deutsch-Mentor",
    page_icon="🇩🇪",
    layout="centered"
)

# 2. Безопасная настройка ИИ (подходит и для сайта, и для компа)
if "API_KEY" in st.secrets:
    API_KEY = st.secrets["API_KEY"]
else:
    # Если запускаешь на компе, он возьмет ключ отсюда:
    API_KEY = "AIzaSyA7fxHcsYgiWPvRCzSlmnef6NQaULdj08I"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-3-flash-preview')

# 3. Словарь переводов
translations = {
    "Deutsch": {"title": "B2 Schreib-Mentor", "sidebar_lang": "Sprache:", "sidebar_topic": "Thema:", "custom_topic": "Eigenes Thema...", "input_label": "Text:", "button": "Prüfen", "status": "KI analysiert...", "placeholder": "Sehr geehrte Damen...", "own_topic_label": "Thema eingeben:"},
    "Українська": {"title": "B2 Наставник", "sidebar_lang": "Мова:", "sidebar_topic": "Тема:", "custom_topic": "Своя тема...", "input_label": "Текст:", "button": "Перевірити", "status": "ШІ аналізує...", "placeholder": "Шановні пані та панове...", "own_topic_label": "Введіть тему:"},
    "Русский": {"title": "B2 Наставник", "sidebar_lang": "Язык:", "sidebar_topic": "Тема:", "custom_topic": "Своя тема...", "input_label": "Текст:", "button": "Проверить", "status": "ИИ анализирует...", "placeholder": "Уважаемые дамы и господа...", "own_topic_label": "Введите тему:"},
    "English": {"title": "B2 Writing Mentor", "sidebar_lang": "Language:", "sidebar_topic": "Topic:", "custom_topic": "Custom Topic...", "input_label": "Text:", "button": "Check", "status": "AI is analyzing...", "placeholder": "Dear Sir or Madam...", "own_topic_label": "Enter topic:"},
    "Türkçe": {"title": "B2 Yazma Rehberi", "sidebar_lang": "Dil:", "sidebar_topic": "Konu:", "custom_topic": "Kendi konum...", "input_label": "Metin:", "button": "Kontrol Et", "status": "Analiz ediliyor...", "placeholder": "Sayın...", "own_topic_label": "Konuyu girin:"},
    "Português": {"title": "Mentor B2", "sidebar_lang": "Idioma:", "sidebar_topic": "Assunto:", "custom_topic": "Próprio tema...", "input_label": "Texto:", "button": "Verificar", "status": "Analisando...", "placeholder": "Prezados...", "own_topic_label": "Digite o tema:"},
    "Italiano": {"title": "Mentore B2", "sidebar_lang": "Lingua:", "sidebar_topic": "Argomento:", "custom_topic": "Altro...", "input_label": "Texto:", "button": "Verifica", "status": "Analisi...", "placeholder": "Gentili...", "own_topic_label": "Inserisci argomento:"}
}

# 4. Интерфейс
lang = st.sidebar.selectbox("🌐 Interface Language", list(translations.keys()))
t = translations[lang]
st.title(f"🇩🇪 {t['title']}")

topics = ["Beschwerde: Sprachkurs", "Bewerbung: Praktikum", "Forumsbeitrag: Homeoffice", t['custom_topic']]
selected_topic = st.sidebar.selectbox(t['sidebar_topic'], topics)

if selected_topic == t['custom_topic']:
    final_topic = st.text_input(t['own_topic_label'], "General Practice")
else:
    final_topic = selected_topic

user_text = st.text_area(t['input_label'], height=300, placeholder=t['placeholder'])

if st.button(t['button']):
    if user_text:
        with st.spinner(t['status']):
            is_custom = "YES" if selected_topic == t['custom_topic'] else "NO"
            prompt = f"Expert German B2 Teacher. Topic: {final_topic}. Custom: {is_custom}. Analyze errors, vocabulary, and score. Answer in {lang}. Text: {user_text}"
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Empty!")
