import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# ✅ حددنا مسار الموديل المحلي
model_path = "models/sentiment"

# ✅ نحمل التوكنيزر والموديل من المسار المحلي
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# ✅ نبني البايبلاين باستخدام الموديل والتوكنيزر المحليين
analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# ✅ الدالة اللي هتستخدم في main.py
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
            st.error(f"An error occurred: {e}")
