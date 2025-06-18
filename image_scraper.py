import requests
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import streamlit as st

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
    return webdriver.Chrome(service=service, options=options)

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

def display_images(image_urls):
    cols = st.columns(2)
    for idx, url in enumerate(image_urls):
        try:
            response = requests.get(url, timeout=10)
            if "image" in response.headers.get("Content-Type", ""):
                img = Image.open(BytesIO(response.content))
                with cols[idx % 2]:
                    st.image(img, caption=f"Image {idx + 1}", use_container_width=True)
        except Exception as e:
            st.warning(f"Error loading image {idx + 1}: {e}")
