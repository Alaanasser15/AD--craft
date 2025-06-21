# preview_page.py
import streamlit as st

def show_preview_page():
    st.title("📝 Preview and Submit Feedback")

    # عرض النصّ التسويقي
    if "generated_text" in st.session_state:
        st.markdown("#### Generated Marketing Content:")
        st.text_area(
            "Your Generated Text",
            value=st.session_state.generated_text,
            height=200
        )

    # عرض الصور المرفوعة
    if "uploaded_files" in st.session_state:
        st.markdown("#### Uploaded Media:")
        for file in st.session_state.uploaded_files:
            if file.type.startswith("image"):
                st.image(file, caption=file.name, use_column_width=True)
            elif file.type.startswith("video"):
                st.video(file)

    # بالالين 🎈
    st.balloons()

    # Feedback
    st.markdown("---")
    st.markdown("#### Feedback Form")
    feedback = st.text_area(
        "Your feedback or additional comments:",
        placeholder="Share your thoughts on the generated content and media."
    )
    if st.button("Submit"):
        if feedback.strip() != "":
            st.success("Thank you for your feedback!")
        else:
            st.warning("Please enter some feedback before submitting.")
