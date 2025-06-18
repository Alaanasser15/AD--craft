import streamlit as st

def upload_media_page():
    st.title("Upload Your Media")
    
    uploaded_files = st.file_uploader(
        "Upload images or videos for your ad:",
        accept_multiple_files=True,
        type=["jpg", "jpeg", "png", "mp4", "mov"]
    )
    
    if uploaded_files:
        st.success(f"You uploaded {len(uploaded_files)} file(s).")
        for file in uploaded_files:
            if file.type.startswith("image"):
                st.image(file, caption=file.name, use_column_width=True)
            elif file.type.startswith("video"):
                st.video(file)
