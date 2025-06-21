import streamlit as st
import base64
import os
from ctransformers import AutoModelForCausalLM

# Import all page components
from image_scraper import scrape_google_images, display_images
from sentiment_analyzer import sentiment_analyzer
from qr_generator import generate_qr_page
from post_scheduler import schedule_post_page
from text_generator import generate_marketing_text
from media_uploader import upload_media_page
from preview_page import show_preview_page

# Load and encode background image
with open("Blue Futuristic Technology Background Instagram Story.png", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# Configure the page
st.set_page_config(page_title="AD CRAFT", layout="wide")

# Custom CSS
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

# Load AI model
llm = AutoModelForCausalLM.from_pretrained(
    "zoltanctoth/orca_mini_3B-GGUF",
    model_file="orca-mini-3b.q4_0.gguf"
)

SYSTEM = "You are an AI assistant that follows instructions extremely well."
chat_history = []

def get_prompt(instruction, history):
    context = ". ".join(history)
    return f"### System:\n{SYSTEM}. Context: {context}\n\n### User:\n{instruction}\n\n### Response:\n"

# Navigation
st.sidebar.title("AD CRAFT Navigation")
page = st.sidebar.radio("Navigate to a feature:", [
    "Write Marketing Content",
    "Find Images Online",
    "Upload Your Media",
    "Generate QR Code",
    "Schedule Your Post",
    "Ask Assistant",
    "Preview and Submit Feedback"
])

# Feature pages
if page == "Write Marketing Content":
    # ... same as before
    pass
elif page == "Find Images Online":
    # ... same as before
    pass
elif page == "Upload Your Media":
    upload_media_page()
elif page == "Generate QR Code":
    generate_qr_page()
elif page == "Schedule Your Post":
    schedule_post_page()
elif page == "Ask Assistant":
    # ... same as before
    pass
elif page == "Preview and Submit Feedback":
    st.title("📝 Preview and Submit Feedback")

    if "generated_text" in st.session_state:
        st.markdown("#### Generated Marketing Content:")
        st.text_area("Your Generated Text", value=st.session_state.generated_text, height=200)

    if "uploaded_files" in st.session_state:
        st.markdown("#### Uploaded Media:")
        for file in st.session_state.uploaded_files:
            if file.type.startswith("image"):
                st.image(file, caption=file.name, use_column_width=True)
            elif file.type.startswith("video"):
                st.video(file)

    st.markdown("---")
    feedback = st.text_area(
        "Your feedback or additional comments:",
        placeholder="Share your thoughts on the generated content and media."
    )

    if st.button("Submit"):
        if feedback.strip() != "":
            st.balloons()
            st.success("Thank you for your feedback!")
        else:
            st.warning("Please enter some feedback before submitting.")
