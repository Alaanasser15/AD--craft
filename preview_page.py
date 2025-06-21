# preview_page.py
import streamlit as st

def show_preview_page():
    st.title("Preview & Feedback")

    st.markdown("## Uploaded Media Preview")
    if "uploaded_image" in st.session_state and st.session_state.uploaded_image is not None:
        st.image(
            st.session_state.uploaded_image,
            caption="Your uploaded image",
            use_column_width=True
        )
    else:
        st.info("No image uploaded yet. Please go to the 'Upload Your Media' page first.")

    # Feedback section
    st.markdown("---")
    st.markdown("## Feedback")
    feedback = st.text_area("Let us know your thoughts or suggestions:")
    if st.button("Submit Feedback"):
        st.success("Thanks for your feedback!")
