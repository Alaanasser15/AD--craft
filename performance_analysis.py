import streamlit as st
import requests
import json
import os
from facebook_scraper import get_posts

# ✅ Debug: Load and test Facebook Cookies
cookies_path = "C:/Users/Computer Store/graduation_project/cookies.txt"
try:
    with open(cookies_path, "r", encoding="utf-8") as f:
        cookies = json.load(f)
        print("✅ Cookies Loaded:", cookies)
except json.JSONDecodeError:
    print("❌ Invalid JSON format in cookies.txt")
except Exception as e:
    print("❌ Error loading cookies:", str(e))

# ✅ Load Facebook Cookies
def load_facebook_cookies():
    try:
        if not os.path.exists(cookies_path):
            return {"error": "❌ Cookies file not found!"}

        with open(cookies_path, "r", encoding="utf-8") as f:
            cookies = json.load(f)  # Load JSON cookies
            return {cookie["name"]: cookie["value"] for cookie in cookies}

    except json.JSONDecodeError:
        return {"error": "❌ Invalid cookies format! Ensure it's in JSON format."}
    except Exception as e:
        return {"error": f"❌ Unexpected error: {str(e)}"}

# ✅ Facebook Post Performance
def get_facebook_post_performance(post_id):
    cookies = load_facebook_cookies()
    if "error" in cookies:
        return cookies  # Return error if cookies fail to load

    try:
        post = next(get_posts(post_id, cookies=cookies))
        return {
            "likes": post.get("likes", 0),
            "shares": post.get("shares", 0),
            "comments": post.get("comments", 0),
            "post_text": post.get("text", "")[:500],  # Limit text to 500 chars
        }
    except Exception as e:
        return {"error": str(e)}

# ✅ Twitter Ad Performance
def get_twitter_ad_performance(ad_id, bearer_token):
    if not bearer_token:
        return {"error": "❌ Bearer Token is required for Twitter API."}

    url = f"https://api.twitter.com/2/tweets/{ad_id}?tweet.fields=public_metrics"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.get(url, headers=headers)

    try:
        data = response.json()
        if "data" in data:
            tweet_data = data["data"]
            return {
                "likes": tweet_data.get("public_metrics", {}).get("like_count", 0),
                "retweets": tweet_data.get("public_metrics", {}).get("retweet_count", 0),
                "replies": tweet_data.get("public_metrics", {}).get("reply_count", 0)
            }
        return {"error": "❌ Invalid Twitter API response"}
    except Exception as e:
        return {"error": str(e)}

# 🎯 Streamlit UI
def main():
    st.title("📊 Facebook & Twitter Ad Performance Analysis")
    platform = st.selectbox("🌐 Select Platform", ["Facebook", "Twitter"])

    if platform == "Facebook":
        post_id = st.text_input("🆔 Enter Facebook Post ID:")
        if st.button("🔍 Get Performance"):
            if post_id:
                data = get_facebook_post_performance(post_id)
                st.json(data)
            else:
                st.warning("⚠️ Please enter a valid Facebook Post ID.")

    elif platform == "Twitter":
        ad_id = st.text_input("🆔 Enter Twitter Tweet ID:")
        bearer_token = st.text_input("🔑 Enter Bearer Token:", type="password")
        if st.button("🔍 Get Performance"):
            if ad_id and bearer_token:
                data = get_twitter_ad_performance(ad_id, bearer_token)
                st.json(data)
            else:
                st.warning("⚠️ Please enter both Twitter Tweet ID and Bearer Token.")

if __name__ == "__main__":
    main()
