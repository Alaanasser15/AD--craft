import streamlit as st
from transformers import pipeline

# ✅ استخدمي المسار الصحيح بعد ما نزلنا بصيغة bin
analyzer = pipeline(
    'sentiment-analysis',
    model="models/sentiment",
    tokenizer="models/sentiment"
)

def sentiment_analyzer():
    st.title('🧠 Sentiment Analyzer')
    st.write("""
        This app classifies the sentiment of the text as Positive or Negative.
        Just type some text below and see the result!
    """)

    user_input = st.text_area('Enter your text here:')

    if user_input:
        try:
            result = analyzer(user_input)

            sentiment = result[0]['label']
            score = result[0]['score']

            if sentiment == 'POSITIVE':
                st.success(f"😊 Sentiment: Positive with a confidence of {score:.2f}")
            elif sentiment == 'NEGATIVE':
                st.error(f"😠 Sentiment: Negative with a confidence of {score:.2f}")
            else:
                st.info(f"😐 Sentiment: {sentiment} with a confidence of {score:.2f}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
