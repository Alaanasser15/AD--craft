from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import uvicorn

app = FastAPI()

def get_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("user-agent=Mozilla/5.0")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def scrape_google_images(query: str, num_images: int = 10):
    driver = get_webdriver()
    image_urls = []
    try:
        url = f"https://www.google.com/search?hl=en&tbm=isch&q={query}"
        driver.get(url)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img")))

        images = driver.find_elements(By.CSS_SELECTOR, "img")
        for img in images:
            src = img.get_attribute("src")
            if src and src.startswith("http") and len(image_urls) < num_images:
                image_urls.append(src)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()
    return image_urls

@app.get("/search")
def search_images(query: str = Query(..., description="Search query"), num: int = 10):
    images = scrape_google_images(query, num)
    return JSONResponse(content={
        "query": query,
        "image_urls": images
    })

if __name__ == "__main__":
    uvicorn.run("image_api:app", host="0.0.0.0", port=8501)
