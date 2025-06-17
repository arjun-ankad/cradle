import os
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# Load FinBERT
model_name = "yiyanghkust/finbert-tone"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Define directories
news_dir = os.path.join(os.path.dirname(__file__), "../data_pipeline/cache/news")
output_dir = os.path.join(os.path.dirname(__file__), "../data_pipeline/cache/sentiment")
os.makedirs(output_dir, exist_ok=True)

# Label mapping
labels = ["Bullish", "Neutral", "Bearish"]

# Classify a headline
def classify_sentiment(title):
    inputs = tokenizer(title, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=1).flatten().tolist()

    # Threshold logic
    neutral_prob = probs[1]
    if neutral_prob > 0.5:
        label = "NEUTRAL"
    elif probs[0] > probs[2]:
        label = "BULLISH"
    else:
        label = "BEARISH"

    return max(probs), label  # Return highest confidence and label

# Loop through each ticker file
for filename in os.listdir(news_dir):
    if not filename.endswith(".csv"):
        continue

    ticker = filename.replace(".csv", "")
    news_path = os.path.join(news_dir, filename)
    df = pd.read_csv(news_path)

    # Prepare output
    results = []
    for _, row in df.iterrows():
        score, label = classify_sentiment(str(row["title"]))
        results.append({
            "timestamp": row["timestamp"],
            "publisher": row["publisher"],
            "score": round(score, 4),
            "label": label
        })

    out_df = pd.DataFrame(results)
    out_path = os.path.join(output_dir, f"{ticker}_sentiment_score.csv")
    out_df.to_csv(out_path, index=False)
    print(f"Saved: {out_path}")