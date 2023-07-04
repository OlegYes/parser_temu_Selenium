import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import fake_useragent
import pickle

def get_coccies():
    # get coocies
    # Set up Selenium WebDriver (make sure you have installed the appropriate WebDriver for your browser)
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={fake_useragent.UserAgent().random}")
    driver = webdriver.Chrome(options=options)  # Replace with the path to your ChromeDriver
    # Navigate to the website
    url = 'https://www.temu.com/'
    driver.get(url)
    time.sleep(120)
    pickle.dump(driver.get_cookies(), open(f"cookies", 'wb'))
    driver.quit()

def parseit():
    try:
        # Set up Selenium WebDriver (make sure you have installed the appropriate WebDriver for your browser)
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={fake_useragent.UserAgent().random}")
        driver = webdriver.Chrome(options=options)  # Replace with the path to your ChromeDriver

        # Navigate to the website
        url = 'https://www.temu.com/'
        driver.get(url)

        # print('open page')
        # Wait for the page to load (you can adjust the sleep duration as needed)
        time.sleep(5)
        for cookie in pickle.load(open(f"cookies", 'rb')):
            driver.add_cookie(cookie)
        # print('load cookies')
        time.sleep(5)
        driver.refresh()
        # print('page refresh')
        time.sleep(5)

        driver.get(url)
        time.sleep(5)
        # Get the page height
        scroll_height = int(driver.execute_script("return document.body.scrollHeight;"))

        print("Page height:", scroll_height)

        # Scroll down the page
        for i in range(0, scroll_height, int(scroll_height/20)):
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(.5)
        time.sleep(2)
        # Create empty lists to store the extracted information
        photos = []
        prices = []
        info = []

        # Find all the product elements on the page
        products = driver.find_elements(By.CLASS_NAME, '_3GizL2ou')
        # Extract the required information for each product
        for product in products:
            # Extract the photo URL
            photo_element= product.find_element(By.TAG_NAME, 'img')
            photo = photo_element.get_attribute('src')
            photos.append(photo)

            # Extract the price
            price_element = product.find_element(By.CLASS_NAME, '_2L24asES')
            price = price_element.text
            prices.append(price)

            # Extract the product information
            info_element = product.find_element(By.CLASS_NAME, '_2XmIMTf3')
            product_info = info_element.text.strip()
            info.append(product_info)

        # Create a DataFrame from the extracted information
        data = {'Photo': photos, 'Price': prices, 'Product Info': info}
        df = pd.DataFrame(data)

        # Save the DataFrame to an Excel file
        df.to_excel('product_info.xlsx', index=False)
        driver.quit()
    except Exception as ex:
            print(ex)
            # Close the browser



if __name__ == "__main__":
    # get_coccies()
    parseit()
