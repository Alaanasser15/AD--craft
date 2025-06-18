import streamlit as st
from datetime import datetime, timedelta
import requests

# Function to format date and time
def format_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def schedule_post_page():
    # Creating the app title with a stylish header
    st.markdown("""
        <h1 style='text-align: center; color: #4CAF50;'>📅 Schedule your social media advertisement</h1>
    """, unsafe_allow_html=True)

    # Section for entering the text of the post
    st.markdown("### ✍️ Enter Your Text Below:")
    user_input = st.text_area("Write your post content here:", height=150)

    # Section for uploading a file (image or video)
    st.markdown("### 📤 Upload a File (Image/Video):")
    uploaded_file = st.file_uploader("Choose a file", type=["mp4", "mov", "avi", "mkv", "jpg", "jpeg", "png"])

    # Date and time selection for scheduling the post
    st.markdown("### ⏰ Select the Date and Time to Schedule the Post:")
    selected_date = st.date_input("Select the Date")
    selected_time = st.time_input("Select the Time")

    # Combine date, time into a datetime object
    scheduled_datetime = datetime.combine(selected_date, selected_time)

    # Display preview and validation
    if user_input:
        if scheduled_datetime < datetime.now():
            st.warning("⚠️ The selected date and time should be in the future.")
        else:
            st.success("✅ Post will be scheduled successfully!")
            # Show the post preview with content and file preview
            st.markdown(f"### ✨ Post Preview")
            st.markdown(f"*Text Entered:* {user_input}")

            # Show uploaded file preview
            if uploaded_file:
                st.markdown("*Uploaded File Preview:*")
                if uploaded_file.type.startswith("image"):
                    st.image(uploaded_file, caption="🖼️ Uploaded Image", use_column_width=True)
                elif uploaded_file.type.startswith("video"):
                    st.video(uploaded_file)

            # Show the scheduled publish date and time
            st.markdown(f"*Scheduled to be Published on:* {format_datetime(scheduled_datetime)}")

            # Calculate and display time remaining until scheduled post
            time_remaining = scheduled_datetime - datetime.now()
            if time_remaining > timedelta(0):
                st.markdown(f"*Time Remaining:* {str(time_remaining).split('.')[0]} until post is published.")
            else:
                st.warning("⚠️ The selected time is in the past.")
