from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

app = FastAPI()

def get_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # ممكن تعلق السطر ده لو عاوز تشوف المتصفح
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("user-agent=Mozilla/5.0")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def scrape_google_images(query: str, limit: int = 1):
    driver = get_webdriver()
    images = []
    try:
        url = f"https://www.google.com/search?hl=en&tbm=isch&q={query}"
        driver.get(url)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.Q4LuWd")))

        img_elements = driver.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
        count = 0
        for img in img_elements:
            src = img.get_attribute("src")
            if src and src.startswith("http") and count < limit:
                images.append({
                    "id": str(count),
                    "url": src
                })
                count += 1
            if count >= limit:
                break

    except Exception as e:
        raise e
    finally:
        driver.quit()

    return images

@app.get("/images/search")
def images_search(query: str = Query(..., description="Search term"),
                  limit: int = Query(1, ge=1, le=20, description="Number of images to return")):
    try:
        results = scrape_google_images(query, limit)
        return JSONResponse(content=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
