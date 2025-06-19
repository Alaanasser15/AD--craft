from transformers import AutoModelForSequenceClassification, AutoTokenizer
import os

model_name = "distilbert-base-uncased-finetuned-sst-2-english"
save_directory = "models/sentiment"

# إنشاء المجلد لو مش موجود
os.makedirs(save_directory, exist_ok=True)

# تحميل النموذج والتوكنيزر
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# حفظهم محلياً
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)

print("✅ Model and tokenizer saved successfully to:", save_directory)
