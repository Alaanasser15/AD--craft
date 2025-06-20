import streamlit as st
from transformers import pipeline

# ✅ استخدمي الموديل المرفوع على Hugging Face
analyzer = pipeline("sentiment-analysis", model="alaanasserrr/ad-craft")

def sentiment_analyzer():
    st.title('🧠 Sentiment Analyzer')
    st.write("This app classifies the sentiment of the text as Positive or Negative.")

    user_input = st.text_area('Enter your text here:')

    if user_input:
        try:
            result = analyzer(user_input)
            label = result[0]["label"]
            score = result[0]["score"]

            if label.upper() == "POSITIVE":
                st.success(f"😊 Sentiment: Positive ({score:.2f})")
            elif label.upper() == "NEGATIVE":
                st.error(f"😠 Sentiment: Negative ({score:.2f})")
            else:
                st.info(f"😐 Sentiment: {label} ({score:.2f})")
        except Exception as e:
            st.error(f"❌ Error: {e}")
