from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch_reviews(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--window-size=1920,1080") # Baray screen size taake reviews load hon
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        
        # 1. Page ko thora scroll karna taake reviews load hon
        driver.execute_script("window.scrollTo(0, 2500);") 
        time.sleep(5) # Wait for reviews to appear
        
        # 2. Mazid scroll (agar reviews niche hon)
        driver.execute_script("window.scrollTo(0, 3500);")
        time.sleep(3)

        reviews = []
        
        # DARAZ REVIEWS KI ASLI CLASSES
        # Hum multiple tareeqon se dhoondein gay
        selectors = [
            "div.pdp-mod-review-item-content",
            "div.item-content",
            "div.content"
        ]
        
        for selector in selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for el in elements:
                text = el.text.strip()
                # Sirf wo text uthao jo "Download app" jaisa na ho
                if len(text) > 10 and "download app" not in text.lower():
                    reviews.append(text)
        
        driver.quit()
        
        # Agar kuch na mile to empty list na bhejein balkay batayen
        return list(set(reviews)) if reviews else []
        
    except Exception as e:
        print(f"Error: {e}")
        return []