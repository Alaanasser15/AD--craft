import streamlit as st
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import torch

# ✅ تحميل النموذج والتوكنيزر من المجلد المحلي
model_path = "models/sentiment/snapshots/714eb0fa89d2f80546fda750413ed43d93601a13"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# ✅ تهيئة البايبلاين
analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1)

# ✅ واجهة ستريملت
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
