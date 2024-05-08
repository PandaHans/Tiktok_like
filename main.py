import os
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import random

options = webdriver.ChromeOptions()
options.add_argument('--log-level=3')
options.add_argument(f"--user-data-dir={os.getcwd()}\\profile")

options.add_argument('--disable-blink-features=AutomationControlled')

# Chrome is controlled by automated test software
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

driver = webdriver.Chrome(options=options, executable_path=CM().install())

driver.set_window_position(0, 0)
driver.set_window_size(414, 936)

url_file = open('urls.txt', "r")
urls = url_file.readlines()

def sleep_randomly():
    delay = random.uniform(0.5, 1.5)
    time.sleep(delay)

time.sleep(5)

# Function to check if there are any more elements with the specified class name
def are_more_elements_present(driver, class_name):
    elements = driver.find_elements(By.CLASS_NAME, class_name)
    return len(elements) > 0

def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("window.scrollBy(0, -100);")

# Function to scroll down the page until there are no more elements with the specified class name
def scroll_until_no_more_elements(driver, class_name, max_scrolls):
    for _ in range(max_scrolls):
        if are_more_elements_present(driver, class_name):
            # Scroll down to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("Scrolling down")
            # Wait for a brief moment for content to load
            time.sleep(2)
        else:
            break


for url in urls:
    print('--Liking comments for this post: ' + url)

    driver.get(url)

    try:
        

        # Wait for the like buttons to be clickable
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-gb2mrc-SpanCount.ezxoskx3')))

        # Scroll down to load all comments
        scroll_until_no_more_elements(driver, 'css-gb2mrc-SpanCount.ezxoskx3', max_scrolls=10)  # Adjust the max_scrolls as needed

        # Find all like buttons
        like_buttons = driver.find_elements(By.CLASS_NAME, 'css-gb2mrc-SpanCount.ezxoskx3')

        # Click on each like button
        for button in like_buttons:
            scroll_into_view(driver, button)
            time.sleep(1)
            button.click()
            print("liked")
            sleep_randomly()

    except NoSuchElementException:
        print('Could not find like buttons.')

print('FINISHED')
driver.quit()