# PySpark Code (in a file named twitter_stream.py)
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Setup SparkSession
spark = SparkSession.builder \
    .appName("TwitterStreamingAnalysis") \
    .getOrCreate()

# Define Schema for Tweets
schema = StructType([
    StructField("created_at", StringType(), True),
    StructField("text", StringType(), True),
    StructField("user", StructType([
        StructField("id", LongType(), True),
        StructField("screen_name", StringType(), True),
        StructField("followers_count", IntegerType(), True)
    ]), True)
])

# Twitter API credentials
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Authenticate to Twitter API
import tweepy

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Define function to stream tweets
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, output_file):
        super().__init__()
        self.output_file = output_file

    def on_status(self, status):
        try:
            data = {
                "created_at": str(status.created_at),
                "text": status.text,
                "user": {
                    "id": status.user.id,
                    "screen_name": status.user.screen_name,
                    "followers_count": status.user.followers_count
                }
            }
            # Write data to the output file
            with open(self.output_file, "a") as file:
                file.write(str(data) + "\n")
        except Exception as e:
            print("Error:", e)

# Start streaming tweets
def start_streaming(output_file, keywords):
    myStreamListener = MyStreamListener(output_file)
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(track=keywords)

# Streamlit App (in a file named streamlit_app.py)
import streamlit as st

# Define function to read tweets from the output file
def read_tweets(file_path):
    tweets = []
    with open(file_path, "r") as file:
        for line in file:
            tweets.append(eval(line))  # Convert string to dictionary
    return tweets

# Main Streamlit app
def main():
    st.title("Live Twitter Streaming Analysis")

    # Start streaming tweets when button is clicked
    if st.button("Start Streaming"):
        output_file = "tweets.txt"  # File to store tweets
        keywords = ['python', 'pyspark', 'data analysis', 'machine learning']
        start_streaming(output_file, keywords)

    # Display streamed tweets
    st.subheader("Streamed Tweets")
    if st.checkbox("Show Tweets"):
        tweets = read_tweets("tweets.txt")
        for tweet in tweets:
            st.write(tweet)

if __name__ == "__main__":
    main()
