import tweepy
from transformers import pipeline
import re

# Twitter API Credentials (Replace with your own)
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAABVDzQEAAAAAUNfucMfuE8%2FWRruONZ6vLZ6RK6M%3D5vIwR2A8UE552dmcIZZU7FoqQgaBcFJwlQtOdyyJllU9AaEV6G"

# Initialize Tweepy API (Twitter API v2)
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Load Pre-trained Sentiment Analysis Model
sentiment_analyzer = pipeline("sentiment-analysis")

def clean_text(text):
    """Remove links, mentions, and special characters from tweets."""
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r'\@\w+|\#','', text)
    return text.strip()

def get_tweets(brand_name, count=10):
    """Fetch recent tweets using Twitter API v2."""
    query = f"{brand_name} -is:retweet lang:en"  # Exclude retweets
    tweets = client.search_recent_tweets(query=query, max_results=count, tweet_fields=["text"])

    if tweets.data:
        return [clean_text(tweet.text) for tweet in tweets.data]
    else:
        return []

def analyze_sentiment(brand_name, count=10):
    """Fetch tweets and analyze their sentiment."""
    tweets = get_tweets(brand_name, count)
    sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
    
    if not tweets:
        print("No tweets found for the brand:", brand_name)
        return sentiment_counts

    for tweet in tweets:
        result = sentiment_analyzer(tweet)[0]  # Analyze sentiment
        label = result['label'].lower()
        if label == "positive":
            sentiment_counts["positive"] += 1
        elif label == "negative":
            sentiment_counts["negative"] += 1
        else:
            sentiment_counts["neutral"] += 1
    
    return sentiment_counts

# Test the model
if __name__ == "__main__":
    brand = input("Enter a brand name: ")
    results = analyze_sentiment(brand, count=20)
    print(f"\nSentiment Analysis for '{brand}':")
    print(f"✅ Positive: {results['positive']}")
    print(f"❌ Negative: {results['negative']}")
    print(f"😐 Neutral: {results['neutral']}")
