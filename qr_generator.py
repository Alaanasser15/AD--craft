import qrcode
import streamlit as st
from io import BytesIO

def generate_qr_code(data: str, box_size: int = 20):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def generate_qr_page():
    st.title("🎨 QR Code Generator")
    st.markdown("Enter text or a URL to generate a high-quality QR code.")

    user_input = st.text_input("🔗 Enter text or URL:", "https://example.com")
    box_size = st.slider("📏 QR Code Size", min_value=10, max_value=40, value=20)

    if st.button("✨ Generate QR Code"):
        qr_image = generate_qr_code(user_input, box_size)
        st.image(qr_image, caption="📌 Your QR Code", use_column_width=True)
        st.download_button("📥 Download QR Code", qr_image, file_name="qrcode.png", mime="image/png")
