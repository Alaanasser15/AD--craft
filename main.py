import streamlit as st
import base64
import os
from ctransformers import AutoModelForCausalLM

# ✅ Import all page components
from image_scraper import scrape_google_images, display_images
from sentiment_analyzer import sentiment_analyzer
from qr_generator import generate_qr_page
from post_scheduler import schedule_post_page
from text_generator import generate_marketing_text
from media_uploader import upload_media_page
from preview_page import show_preview_page

# ✅ Check if running on Streamlit Cloud
IS_CLOUD = os.environ.get("STREAMLIT_SERVER_PORT") == "8501"

# ✅ Load and encode wallpaper background
with open("Blue Futuristic Technology Background Instagram Story.png", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# ✅ Set Streamlit page configuration
st.set_page_config(page_title="AD CRAFT", layout="wide")

# ✅ Custom CSS for background and theme
st.markdown(f"""<style>/* CSS STYLES HERE */</style>""", unsafe_allow_html=True)  # اختصرته هنا للتوضيح

# ✅ Load the chatbot model
llm = AutoModelForCausalLM.from_pretrained(
    "zoltanctoth/orca_mini_3B-GGUF",
    model_file="orca-mini-3b.q4_0.gguf"
)

SYSTEM = """You are an AI assistant..."""

chat_history = []
def get_prompt(instruction, history):
    context = ". ".join(history)
    return f"### System:\n{SYSTEM}. Context: {context}\n\n### User:\n{instruction}\n\n### Response:\n"

# ✅ Sidebar navigation
st.sidebar.title("AD CRAFT Navigation")
page = st.sidebar.radio("Navigate to a feature:", [
    "Write Marketing Content",
    "Find Images Online",
    "Create a Video",
    "Upload Your Media",
    "Generate QR Code",
    "Schedule Your Post",
    "Ask Assistant",
    "Preview and Submit Feedback"
])

# ✅ 1. Marketing Text Generator
if page == "Write Marketing Content":
    ...

# ✅ 2. Image Scraper
elif page == "Find Images Online":
    ...

# ✅ 3. Video Generator
elif page == "Create a Video":
    st.title("🎥 Create a Video")

    if IS_CLOUD:
        st.warning("⚠️ Video/GIF generation is disabled on Streamlit Cloud due to resource limits. Please run the app locally to use this feature.")
    else:
        from video_generator import generate_video  # ✅ داخل الكتلة فقط

        prompt = st.text_input("Enter your video idea:")
        base = st.selectbox("Choose style:", ["Cartoon", "Realistic", "3d", "Anime"], index=1)
        motion = st.selectbox("Add motion effect (optional):", [
            "", "Zoom in", "Zoom out", "Tilt up", "Tilt down",
            "Pan left", "Pan right", "Roll left", "Roll right"
        ])
        steps = st.slider("Video quality (steps):", min_value=1, max_value=8, value=4)

        if st.button("Generate Video"):
            if prompt:
                with st.spinner("Generating video..."):
                    video_path = generate_video(prompt, base, motion, steps)
                    st.success("Video generated:")
                    st.video(video_path)
                    st.session_state.generated_video = video_path
            else:
                st.error("Enter a prompt.")

# ✅ 4-8. باقي الصفحات
elif page == "Upload Your Media":
    upload_media_page()
elif page == "Generate QR Code":
    generate_qr_page()
elif page == "Schedule Your Post":
    schedule_post_page()
elif page == "Ask Assistant":
    ...
elif page == "Preview and Submit Feedback":
    show_preview_page()
