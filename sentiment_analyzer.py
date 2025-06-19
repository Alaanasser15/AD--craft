from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import streamlit as st

model_path = "models/sentiment"  # ده المجلد اللي فيه الموديل والملفات

# نحمل التوكنيزر والنموذج من المجلد
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(
    model_path,
    from_safetensors=True  # 💡 دي أهم سطر لازم يتكتب علشان البرنامج يعرف إن الوزنات من النوع safetensors
)

# نجهز الـ pipeline
analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

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
