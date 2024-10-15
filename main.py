import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

request = requests.get('https://appbrewery.github.io/Zillow-Clone/')

page = BeautifulSoup(request.text, features='html.parser')

all_houses = page.find_all('a', class_='StyledPropertyCardDataArea-anchor')

all_prices = page.find_all('span', class_="PropertyCardWrapper__StyledPriceLine")

links = []

addresses = []

prices = []

for house in all_houses:
    # print(house, end="\n" * 2)
    link = house.get('href')
    if link:
        links.append(link)
    address = house.find('address')
    if address:
        addresses.append(address.text.strip())

for price in all_prices:
    prices.append(price.text.strip().replace('+', '').replace('/mo', '').replace('1 bd', ''))

try:
    driver = webdriver.Chrome()
    driver.get(
        'https://docs.google.com/forms/d/e/1FAIpQLSdOKlV3slvjoQ0hWSwPPHnAbkEF5B6cCDMSkfdZKbw0Xu4g4w/viewform?usp=sf_link')

    for price, address, link in zip(prices, addresses, links):
        address_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'))
        )
        address_input.send_keys(address)

        price_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'))
        )
        price_input.send_keys(price)

        link_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'))
        )
        link_input.send_keys(link)

        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, 'html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span'))
        )
        submit_button.click()

        time.sleep(7)  # You can adjust or remove this if needed

        try:
            # Check if we are on the confirmation page
            send_another_response_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a'))
            )
            send_another_response_button.click()  # Click the button to return to the form

            # Wait for the original form to load again
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/form'))
                # Adjust this XPath as necessary
            )

        except WebDriverException:
            print("Did not find the 'Send another response' button, moving to the next iteration.")

        time.sleep(5)

except WebDriverException as e:
    print(f"WebDriver error: {e}")
finally:
    time.sleep(5)  # Keep the browser open for 5 seconds after completion
    driver.quit()
