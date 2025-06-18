# api.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("user-agent=Mozilla/5.0 ...")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def scrape_google_images(query: str, num_images: int = 10):
    driver = get_webdriver()
    image_urls = []

    try:
        driver.get(f"https://www.google.com/search?hl=en&tbm=isch&q={query}")
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img")))
        images = driver.find_elements(By.CSS_SELECTOR, "img")

        for img in images:
            if len(image_urls) >= num_images:
                break
            src = img.get_attribute("src")
            if src and src.startswith("http"):
                image_urls.append(src)
            time.sleep(1)

    finally:
        driver.quit()
    return image_urls

@app.get("/search_images/")
async def search_images(query: str, num_images: int = 10):
    try:
        image_urls = scrape_google_images(query, num_images)
        if not image_urls:
            return JSONResponse(status_code=404, content={"message": "No images found."})
        return {"image_urls": image_urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
