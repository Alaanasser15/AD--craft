import streamlit as st

def show_preview_page():
    st.title("🎯 Preview & Feedback")

    # ✅ عرض النص التسويقي
    if "generated_text" in st.session_state and st.session_state.generated_text:
        st.subheader("📝 Generated Marketing Text:")
        st.write(st.session_state.generated_text)

    # ✅ عرض الصور المسترجعة من Pexels
    if "image_urls" in st.session_state and st.session_state.image_urls:
        st.subheader("🖼️ Selected Images:")
        cols = st.columns(3)
        for i, img_url in enumerate(st.session_state.image_urls):
            cols[i % 3].image(img_url, use_column_width=True)

    # ✅ عرض الفيديو المولَّد (في حال وجوده)
    if "generated_video" in st.session_state:
        st.subheader("🎥 Generated Video:")
        st.video(st.session_state.generated_video)

    # ✅ عرض الملفات المرفوعة من المستخدم
    if "uploaded_files" in st.session_state and st.session_state.uploaded_files:
        st.subheader("📂 Uploaded Media:")
        for file_name in st.session_state.uploaded_files:
            st.write(f"- {file_name}")

    # ✅ عرض QR إذا كان مولد
    if "qr_code_path" in st.session_state and st.session_state.qr_code_path:
        st.subheader("🔗 Generated QR Code:")
        st.image(st.session_state.qr_code_path)

    st.markdown("---")

    # ✅ مساحة الملاحظات
    feedback = st.text_area("💭 Leave your feedback:")
    if st.button("Submit Feedback"):
        if feedback.strip():
            st.success("🎉 Thank you for your feedback!")
        else:
            st.warning("⚠️ Please enter some feedback before submitting.")

