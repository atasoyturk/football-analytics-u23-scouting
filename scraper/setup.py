
from selenium import webdriver  
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.chrome.options import Options  
from webdriver_manager.chrome import ChromeDriverManager  
from config import BRAVE_PATH  


def setup_browser():

    chrome_options = Options()
    chrome_options.add_argument('--headless')  
    
    chrome_options.add_argument('--no-sandbox')  
    
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.7390.55 Safari/537.36'
    )
    
    chrome_options.binary_location = BRAVE_PATH  
    CHROME_DRIVER_PATH = r"C:\Users\User\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe"

    service = Service(CHROME_DRIVER_PATH)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver
