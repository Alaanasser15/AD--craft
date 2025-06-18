import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from webdriver_manager.chrome import ChromeDriverManager

# Function to initialize WebDriver
def get_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")

    # Set a User-Agent to bypass bot detection
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        st.error(f"Error initializing WebDriver: {e}")
        return None

# Function to check if URL is a direct video file
def is_video(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        content_type = response.headers.get("Content-Type", "")
        return "video" in content_type  # Check if it's a video
    except requests.exceptions.RequestException:
        return False

# Function to scrape Bing Videos (excluding YouTube & Vimeo)
def scrape_bing_videos(query, num_videos=5):
    driver = get_webdriver()
    if not driver:
        return []

    try:
        search_url = f"https://www.bing.com/videos/search?q={query}"
        driver.get(search_url)

        # Wait for video results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.mc_vtvc_link"))
        )

        video_urls = []
        video_links = driver.find_elements(By.CSS_SELECTOR, "a.mc_vtvc_link")

        for link in video_links:
            href = link.get_attribute("href")
            if href and "youtube.com" not in href and "vimeo.com" not in href:  # Exclude YouTube/Vimeo
                if is_video(href):  # Check if it's a direct video file
                    video_urls.append(href)

            if len(video_urls) >= num_videos:
                break  # Stop after collecting enough

        return video_urls

    except Exception as e:
        st.error