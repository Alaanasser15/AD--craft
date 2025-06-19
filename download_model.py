from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_id = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
save_path = "models/sentiment"

# Download and save model and tokenizer locally
AutoTokenizer.from_pretrained(model_id).save_pretrained(save_path)
AutoModelForSequenceClassification.from_pretrained(model_id).save_pretrained(save_path)
