import streamlit as st

def upload_media_page():
    uploaded_files = st.file_uploader(
        "Upload your images or videos:", accept_multiple_files=True
    )
    if uploaded_files:
        st.success(f"{len(uploaded_files)} files uploaded successfully!")
        # جهّزي قائمة فيها بيانات الملفات
        file_data_list = []
        for file in uploaded_files:
            file_bytes = file.read()
            file_data_list.append({"data": file_bytes, "type": file.type})
        st.session_state.uploaded_files = file_data_list
