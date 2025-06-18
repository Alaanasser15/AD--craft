import streamlit as st
from googletrans import Translator
import base64
import os
from streamlit_option_menu import option_menu

# ✅ Set background image function (updated with new image path)
def set_background(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            img_bytes = img_file.read()
            encoded_img = base64.b64encode(img_bytes).decode()

        st.markdown(f"""
            <style>
                [data-testid="stAppViewContainer"] {{
                    background-image: url("data:image/png;base64,{encoded_img}");
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    min-height: 100vh;
                }}
                [data-testid="stHeader"], [data-testid="stSidebar"] {{
                    background: transparent;
                }}
                h1 {{
                    font-size: 40px !important;
                    margin-bottom: 5px !important;
                    margin-top: 10px !important;
                }}
                h2, h3 {{
                    font-size: 28px !important;
                }}
                p {{
                    font-size: 18px;
                    line-height: 1.6;
                }}
                body, h1, h2, h3, p, div, span, .stTextInput > label, .stSelectbox > label {{
                    font-family: 'Roboto', sans-serif !important;
                    color: white;
                    text-shadow: 1px 1px 2px #000;
                }}
                .stButton > button {{
                    background-color: #007BFF;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                    border-radius: 8px;
                    width: 100%;
                    font-family: 'Roboto', sans-serif !important;
                    transition: 0.3s;
                }}
                .stButton > button:hover {{
                    background-color: #0056b3;
                }}
                .stButton > button:active {{
                    background-color: #004085;
                }}
                .stTextInput, .stSelectbox, .stFileUploader, .stDateInput, .stTimeInput {{
                    padding: 10px;
                    margin-top: 10px;
                }}
                .centered-text {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 80vh;
                    text-align: center;
                    flex-direction: column;
                    padding: 20px;
                }}
                /* Adding animation for quote texts */
                .quote {{
                    max-width: 800px;
                    margin: 20px;
                    padding: 20px 30px;
                    border-radius: 20px;
                    background: rgba(255, 255, 255, 0.1);
                    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
                    font-size: 24px;
                    line-height: 1.6;
                    backdrop-filter: blur(10px);
                    animation: fadeInUp 1.2s ease both;
                }}
                .quote:nth-child(2) {{
                    font-size: 20px;
                    background: rgba(255, 255, 255, 0.08);
                    animation-delay: 0.4s;
                }}
                @keyframes fadeInUp {{
                    from {{
                        opacity: 0;
                        transform: translateY(30px);
                    }}
                    to {{
                        opacity: 1;
                        transform: translateY(0);
                    }}
                }}
            </style>
        """, unsafe_allow_html=True)
    else:
        st.error("Background image not found!")

# ✅ Apply background
set_background("Blue Futuristic Technology Background Instagram Story.png")

# ✅ Function for Q & A responses
def answer_response(user_input, lang='en'):
    responses = {
        "How can the Answer help me market my product?": "The Answer assists with marketing by automating customer inquiries, sending special offers, collecting customer data, and scheduling promotions.",
        "Can the Answer reply to customers on my behalf?": "Yes! It can answer FAQs, guide customers, and assist with purchases 24/7.",
        "Can the Answer help me sell products?": "Absolutely! It organizes product displays, responds to inquiries, and directs customers to purchase.",
        "Can I use the Answer to send offers to customers?": "Yes, you can automate messages with exclusive offers and discounts.",
        "Can the Answer handle multiple customer inquiries at the same time?": "Yes! Unlike humans, the Answer can chat with multiple customers simultaneously.",
        "How can I create a successful ad campaign?": "Identify your audience, set clear goals, use the right platform, create engaging content, and track performance.",
        "What is ad retargeting? How do I use it?": "Ad retargeting shows ads to users who interacted with your brand before, increasing conversions."
    }
    response = responses.get(user_input, "Sorry, I don't understand that question.")

    translator = Translator()
    translated_response = translator.translate(response, dest=lang).text

    return translated_response

# ✅ Page control with next, back, skip
if "page_index" not in st.session_state:
    st.session_state.page_index = 0

ad_text_global = st.session_state.get("ad_text", "")

def next_page():
    st.session_state.page_index += 1

def prev_page():
    if st.session_state.page_index > 0:
        st.session_state.page_index -= 1

def skip_page():
    st.session_state.page_index = len(pages) - 1

pages = [
    "Welcome",
    "Ad Text",
    "Image Source",
    "GIF Generation",
    "Upload Image",
    "Upload Video",
    "QR Code",
    "Ad Schedule",
    "chatbot",
    "Preview",
    "Thanks"
]

selected = pages[st.session_state.page_index]

st.markdown(f"<div class='centered-text'><h1>{selected}</h1></div>", unsafe_allow_html=True)

# ✅ Pages
if selected == "Welcome":
    st.markdown("""
    <div class='centered-text'>
        <div class="quote">Your go-to app for advertising services.<br>Designed for simplicity and efficiency, we make advertising easier than ever.<br>Get started today and make your business grow with us 🚀</div>
    </div>
    """, unsafe_allow_html=True)

elif selected == "Ad Text":
    ad_text = st.text_area("Type your advertisement content here:", value=ad_text_global)
    if ad_text:
        st.session_state.ad_text = ad_text
        st.markdown(f"<div class='centered-text'><p>{ad_text}</p></div>", unsafe_allow_html=True)

elif selected == "Image Source":
    if st.button("Search on Google"):
        st.info("This would open image search functionality (to be implemented).")

elif selected == "GIF Generation":
    if st.button("Generate AI GIF"):
        st.info("AI GIF generation preview will appear here.")

elif selected == "Upload Image":
    image_file = st.file_uploader("Upload an image for your ad", type=["jpg", "jpeg", "png"])
    if image_file:
        st.image(image_file, caption="Uploaded Image Preview", use_column_width=True)

elif selected == "Upload Video":
    video_file = st.file_uploader("Upload a video for your ad", type=["mp4", "mov"])
    if video_file:
        st.video(video_file)

elif selected == "QR Code":
    qr_data = st.text_input("Enter URL or data for the QR code:")
    if qr_data:
        st.info(f"QR code preview would be generated for: {qr_data}")

elif selected == "Ad Schedule":
    date = st.date_input("Select the date:")
    time = st.time_input("Select the time:")
    if date and time:
        st.success(f"Ad scheduled for {date} at {time}")

elif selected == "Q&A":
    questions = [
        "How can the Answer help me market my product?",
        "Can the Answer reply to customers on my behalf?",
        "Can the Answer help me sell products?",
        "Can I use the Answer to send offers to customers?",
        "Can the Answer handle multiple customer inquiries at the same time?",
        "How can I create a successful ad campaign?",
        "What is ad retargeting? How do I use it?"
    ]
    question = st.selectbox("Choose a question to get an answer:", questions)
    if question:
        answer = answer_response(question)
        st.markdown(f"<div class='centered-text'><p>{answer}</p></div>", unsafe_allow_html=True)

elif selected == "Preview":
    st.markdown(f"""
    <div class='centered-text'>
        <h2>Ad Preview</h2>
        <p>{st.session_state.get("ad_text", "No ad text provided.")}</p>
    </div>
    """, unsafe_allow_html=True)

elif selected == "Thanks":
    st.markdown("""
    <div class='centered-text'>
        <div class="quote">🎉 Thank You for Using AD CRAFT! 🎈🎈<br>We appreciate your time. Happy Advertising!</div>
    </div>
    """, unsafe_allow_html=True)

# ✅ Navigation Buttons
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.session_state.page_index > 0:
        st.button("⬅️ Back", on_click=prev_page)
with col2:
    if st.session_state.page_index < len(pages) - 1:
        st.button("⏭️ Next", on_click=next_page)
with col3:
    if st.session_state.page_index < len(pages) - 1:
        st.button("⏩ Skip to End", on_click=skip_page)
