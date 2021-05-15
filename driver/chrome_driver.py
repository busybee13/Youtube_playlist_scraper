import platform
import os


from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class ChromeDriver():
    
    def loadDriver(proxy = ""):
        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--lang=en-US')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("--output=/dev/null")

        prefs = {
                # "profile.managed_default_content_settings.images": 2, 
                "plugins.plugins_disabled": ["Shockwave Flash"],
                "useAutomationExtension": False}
        chrome_options.add_experimental_option("prefs", prefs)   

        chrome_cap = DesiredCapabilities().CHROME
        chrome_cap["pageLoadStrategy"] = "eager" # This is used to make loading pages faster without waiting for the images and subframes
        
        if platform.system() == 'Linux': 
            driver = webdriver.Chrome(options=chrome_options)
        else:
            chromedriver_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'chromedriver.exe')
            driver = webdriver.Chrome(desired_capabilities=chrome_cap,
                                options=chrome_options,
                                executable_path=chromedriver_path)

        driver.set_page_load_timeout(5) # Avoid unlimited page load hang

        return driver

