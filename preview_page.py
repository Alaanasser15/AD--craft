# preview_page.py

import streamlit as st

def show_preview_page():
    st.title("Final Preview and Feedback")

    st.subheader("1. Marketing Text")
    if 'generated_text' in st.session_state:
        st.text_area("Marketing Text", value=st.session_state.generated_text, height=200)
    else:
        st.info("No marketing text generated yet.")

    st.subheader("2. Uploaded or Scraped Images")
    if 'image_urls' in st.session_state:
        for url in st.session_state.image_urls:
            st.image(url, use_column_width=True)
    else:
        st.info("No images uploaded or scraped.")

    st.subheader("3. Uploaded Media Files")
    if 'uploaded_files' in st.session_state:
        for file in st.session_state.uploaded_files:
            if file.type.startswith("image"):
                st.image(file, caption=file.name, use_column_width=True)
            elif file.type.startswith("video"):
                st.video(file)
    else:
        st.info("No media files uploaded.")

    st.subheader("4. Generated Video")
    if 'generated_video' in st.session_state:
        st.video(st.session_state.generated_video)
    else:
        st.info("No video generated.")

    st.subheader("Your Feedback")
    feedback = st.text_area("Tell us what you think or how we can improve:")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")
