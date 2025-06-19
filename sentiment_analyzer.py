import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# المسار المحلي للموديل
model_path = "models/sentiment"

# تحميل التوكنيزر والموديل من الملفات المحلية
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# إنشاء كائن البايبلاين
analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# دالة Streamlit
def sentiment_analyzer():
    st.title("🧠 Sentiment Analyzer")
    st.write("This app classifies your text as Positive or Negative sentiment.")

    user_input = st.text_area("Enter text here:")

    if user_input:
        result = analyzer(user_input)
        label = result[0]["label"]
        score = result[0]["score"]

        if label == "POSITIVE":
            st.success(f"😊 Positive ({score:.2f} confidence)")
        elif label == "NEGATIVE":
            st.error(f"😠 Negative ({score:.2f} confidence)")
        else:
            st.info(f"😐 {label} ({score:.2f} confidence)")
