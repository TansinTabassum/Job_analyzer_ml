from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import torch

tokenizer = DistilBertTokenizerFast.from_pretrained("model")
model = DistilBertForSequenceClassification.from_pretrained("model")

def predict(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()

    label_map = {
    0: "AI",
    1: "Data",
    2: "Web",
    3: "other"
}

    return label_map[predicted_class]