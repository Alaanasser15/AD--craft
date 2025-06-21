import streamlit as st
import base64
import os
from ctransformers import AutoModelForCausalLM

# ✅ استيراد مكونات الصفحات
from image_scraper import scrape_google_images, display_images
from sentiment_analyzer import sentiment_analyzer
from qr_generator import generate_qr_page
from post_scheduler import schedule_post_page
from text_generator import generate_marketing_text
from media_uploader import upload_media_page
from preview_page import show_preview_page

# ✅ تحميل الخلفية
with open("Blue Futuristic Technology Background Instagram Story.png", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# ✅ إعداد الصفحة
st.set_page_config(page_title="AD CRAFT", layout="wide")

# ✅ CSS مخصص
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white !important;
    }}

    section[data-testid="stSidebar"] {{
        background-color: rgba(0, 40, 80, 0.9);
        color: white !important;
    }}

    section[data-testid="stSidebar"] * {{
        color: white !important;
    }}

    .stTextInput > div > div > input,
    .stTextArea > div > textarea,
    .stSlider > div,
    .stSelectbox > div,
    .stButton > button,
    .stNumberInput input,
    label, .stSlider > label,
    .css-1cypcdb, .css-10trblm, .css-qcqlej,
    .css-1v3fvcr, .css-1y4p8pa, .css-1y4p8pa * {{
        color: white !important;
    }}

    .stTextInput > div > div > input,
    .stTextArea > div > textarea,
    .stNumberInput input {{
        background-color: rgba(255, 255, 255, 0.1) !important;
    }}

    .stButton > button {{
        background-color: #004080 !important;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        transition: background-color 0.2s ease;
    }}

    .stButton > button:hover {{
        background-color: #0066cc !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ✅ تحميل موديل الشات
llm = AutoModelForCausalLM.from_pretrained(
    "zoltanctoth/orca_mini_3B-GGUF",
    model_file="orca-mini-3b.q4_0.gguf"
)

SYSTEM = "You are an AI assistant that follows instructions extremely well. Help as much as you can. Give short answers. Use the context provided and don't mention that you use the context."
chat_history = []

def get_prompt(instruction, history):
    context = ". ".join(history)
    return f"### System:\n{SYSTEM}. Context: {context}\n\n### User:\n{instruction}\n\n### Response:\n"

# ✅ التنقل
st.sidebar.title("AD CRAFT Navigation")
page = st.sidebar.radio(
    "Navigate to a feature:", [
        "Write Marketing Content",
        "Find Images Online",
        "Upload Your Media",
        "Generate QR Code",
        "Schedule Your Post",
        "Ask Assistant",
        "Preview and Submit Feedback"
    ]
)

# ✅ الصفحات
if page == "Write Marketing Content":
    st.title("🖍️ Write Marketing Content")
    prompt = st.text_area("Describe your product or service:")
    max_length = st.slider("Maximum length of the generated content:", 50, 500, 150)
    if st.button("Generate Text"):
        if prompt:
            with st.spinner("Generating content..."):
                generated_text = generate_marketing_text(prompt, max_length)
                st.success("Generated marketing content:")
                st.text_area("Generated Text", value=generated_text, height=300)
                st.session_state.generated_text = generated_text
        else:
            st.warning("Enter a description.")

elif page == "Find Images Online":
    st.title("🖼️ Find Images Online")
    query = st.text_input("Enter a search term:")
    if query:
        urls = scrape_google_images(query)
        if urls:
            st.session_state.image_urls = urls
            st.success(f"Found {len(urls)} images.")
    if "image_urls" in st.session_state:
        display_images(st.session_state.image_urls)

elif page == "Upload Your Media":
    upload_media_page()

elif page == "Generate QR Code":
    generate_qr_page()

elif page == "Schedule Your Post":
    schedule_post_page()

elif page == "Ask Assistant":
    st.title("💬 Ask the Assistant")
    user_input = st.text_input("Type your question here:")
    if st.button("Ask"):
        if user_input:
            prompt = get_prompt(user_input, chat_history)
            chat_history.append(user_input)
            with st.spinner("Thinking..."):
                response = "".join(token for token in llm(prompt, stream=True))
                chat_history.append(response)
                st.success("Assistant's Response:")
                st.markdown(response)
        else:
            st.warning("Please enter a question.")

    st.markdown("---")
    with st.container():
        st.markdown("### 📘 Common Marketing Questions")
        selected_faq = st.selectbox(
            "Select a question:",
            [
                "What is a marketing funnel?",
                "How do I target the right audience?",
                "What is A/B testing?",
                "How can I improve engagement on my posts?",
                "What is SEO and why is it important?",
                "What are KPIs in marketing?",
                "What is content marketing?",
                "What is the difference between B2B and B2C marketing?",
                "How do I measure social media ROI?",
                "Why is branding important in marketing?"
            ]
        )
        faq_answers = {
            "What is a marketing funnel?": "A marketing funnel represents the journey potential customers go through from awareness to conversion.",
            "How do I target the right audience?": "Identify your ideal customer persona using data like demographics, interests, and behavior.",
            "What is A/B testing?": "A/B testing is a method to compare two versions of content to determine which performs better.",
            "How can I improve engagement on my posts?": "Use high-quality visuals, strong CTAs, and post at optimal times based on your audience analytics.",
            "What is SEO and why is it important?": "Search Engine Optimization improves your content visibility in search engines, increasing organic traffic.",
            "What are KPIs in marketing?": "Key Performance Indicators are metrics used to evaluate the success of a marketing campaign.",
            "What is content marketing?": "Content marketing involves creating valuable content to attract and retain a target audience.",
            "What is the difference between B2B and B2C marketing?": "B2B targets businesses; B2C targets individual consumers, with different messaging and channels.",
            "How do I measure social media ROI?": "Track metrics like engagement, conversions, and sales attributed to your social media campaigns.",
            "Why is branding important in marketing?": "Branding builds recognition, trust, and emotional connection with your audience, driving loyalty."
        }
        if selected_faq:
            st.info(faq_answers[selected_faq])

elif page == "Preview and Submit Feedback":
    show_preview_page()
