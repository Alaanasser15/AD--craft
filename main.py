import streamlit as st
import base64
import os
import requests

# === Functions for image search using Pexels API ===
PEXELS_API_KEY = "akPgXcx3oPV87FhSkiwQ8AO6tZsE8tOUacyL13wQh59QrAqXU5MiFT2L"

def scrape_google_images(query):
    """Fetch image URLs using Pexels API"""
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=12"
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return [photo["src"]["medium"] for photo in response.json().get("photos", [])]
    return []

def display_images(image_urls):
    """Display images in columns"""
    cols = st.columns(3)
    for i, img_url in enumerate(image_urls):
        cols[i % 3].image(img_url, use_column_width=True)

# === Dummy page components ===
def sentiment_analyzer(): st.write("Sentiment Analyzer placeholder")
def generate_qr_page(): st.write("QR code generator placeholder")
def schedule_post_page(): st.write("Post scheduler placeholder")
def generate_marketing_text(prompt, max_length): return f"Generated marketing text for: {prompt}"
def upload_media_page(): st.write("Media uploader placeholder")
def show_preview_page(): st.write("Preview page placeholder")

# === Load background image ===
with open("Blue Futuristic Technology Background Instagram Story.png", "rb") as img:
    encoded_image = base64.b64encode(img.read()).decode()

st.set_page_config(page_title="AD CRAFT", layout="wide")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white !important;
    }}
    section[data-testid="stSidebar"] {{
        background-color: rgba(0,40,80,0.9);
        color: white !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: white !important;
    }}
    </style>
""",
    unsafe_allow_html=True,
)

# === Sidebar navigation ===
st.sidebar.title("AD CRAFT Navigation")
page = st.sidebar.radio(
    "Navigate to a feature:",
    [
        "Write Marketing Content",
        "Find Images Online",
        "Create a Video",
        "Upload Your Media",
        "Generate QR Code",
        "Schedule Your Post",
        "Preview and Submit Feedback",
    ],
)

# === Pages content ===
if page == "Write Marketing Content":
    st.title("🖍️ Write Marketing Content")
    prompt = st.text_area("Describe your product or service:")
    max_length = st.slider("Maximum length of the generated content:", 50, 500, 150)
    if st.button("Generate Text") and prompt:
        generated_text = generate_marketing_text(prompt, max_length)
        st.success("Generated marketing content:")
        st.text_area("Generated Text", value=generated_text, height=200)

elif page == "Find Images Online":
    st.title("🖼️ Find Images Online")
    query = st.text_input("Enter a search term:")
    if query:
        urls = scrape_google_images(query)
        if urls:
            st.session_state.image_urls = urls
            st.success(f"Found {len(urls)} images:")
    if "image_urls" in st.session_state:
        display_images(st.session_state.image_urls)

elif page == "Create a Video":
    st.title("🎥 Create a Video")
    st.info("⏳ Processing... Video generation is only available locally due to resource limits.")

elif page == "Upload Your Media":
    upload_media_page()

elif page == "Generate QR Code":
    generate_qr_page()

elif page == "Schedule Your Post":
    schedule_post_page()

elif page == "Preview and Submit Feedback":
    show_preview_page()
