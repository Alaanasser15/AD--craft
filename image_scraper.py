# image_scraper.py
import requests
import streamlit as st

API_KEY = "akPgXcx3oPV87FhSkiwQ8AO6tZsE8tOUacyL13wQh59QrAqXU5MiFT2L"

def scrape_google_images(query):
    # إذا كان المستخدم بيدور على modern academy
    if "academy" in query.lower() or "maadi" in query.lower():
        query = "Modern Academy Maadi Nabil Dabis"
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=12"
    headers = {"Authorization": API_KEY}
    response = requests.get(url, headers=headers)

    image_urls = []
    if response.status_code == 200:
        data = response.json()
        image_urls = [photo["src"]["medium"] for photo in data.get("photos", [])]

    return image_urls

def display_images(image_urls):
    cols = st.columns(3)
    for i, img_url in enumerate(image_urls):
        cols[i % 3].image(img_url, use_column_width=True)
