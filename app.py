import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
from io import BytesIO
from PIL import Image
import json

def get_webdriver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_google_images(query, num_images=10):
    driver = get_webdriver()
    image_urls = []
    try:
        search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={query}"
        driver.get(search_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img"))
        )
        images = driver.find_elements(By.CSS_SELECTOR, "img")
        for img in images:
            if len(image_urls) >= num_images:
                break
            src = img.get_attribute("src")
            if src and src.startswith("http"):
                image_urls.append(src)
    except Exception as e:
        st.error(f"Error during scraping: {e}")
    finally:
        driver.quit()
    return image_urls[:num_images]

def is_image(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        if "image" in response.headers["Content-Type"]:
            return True
    except:
        return False
    return False

# ==== Streamlit UI & API ====

st.title("Google Image Scraper with JSON and Images")

query_params = st.query_params
use_api = "api" in query_params and query_params["api"][0] == "1"
query_input = None

# If API mode, read query from URL params instead of UI
if use_api and "query" in query_params and query_params["query"]:
    query_input = query_params["query"][0]
else:
    query_input = st.text_input("Enter a search query:")

if query_input:
    image_urls = scrape_google_images(query_input)
    result_json = {
        "query": query_input,
        "image_urls": image_urls
    }

    if use_api:
        # Return clean JSON (not as text, but as proper JSON)
        st.json(result_json)
        # Optional: For curl/wget compatibility, you could add:
        # st.write(json.dumps(result_json, indent=2))
    else:
        st.subheader("JSON Result:")
        st.json(result_json)

        st.subheader("Images:")
        cols = st.columns(2)
        for idx, url in enumerate(image_urls):
            if is_image(url):
                try:
                    response = requests.get(url, timeout=10)
                    img = Image.open(BytesIO(response.content))
                    with cols[idx % 2]:
                        st.image(img, caption=f"Image {idx + 1}", use_container_width=True)
                except Exception as e:
                    st.warning(f"Error loading image {idx + 1}: {e}")
else:
    st.info("Please enter a search query to get image URLs and images.")