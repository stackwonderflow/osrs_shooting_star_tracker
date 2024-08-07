from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

def scrape_data(driver):
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    locations = []  # array to store the locations
    worlds = []  # array to store the world numbers
    size = [] # array to store star size
    time = [] # array to store the time in existance

    # Find all 'td' with class 'specialwidth' elements
    for td_special in soup.find_all('td', class_='specialwidth'):
        locations.append(td_special.text.strip())

    # Find all 'td' elements that contain an 'img' with class 'worldicon'
    for td in soup.find_all('td'):
        img = td.find('img', class_='worldicon')
        if img:
            # Extract the integer from the text of the 'td'
            int_value = int(td.text.strip())
            worlds.append(int_value)

    # Find all 'td' elements in 3rd (2) column
    for row in soup.find_all('tr'):
        cell = row.find_all('td')
        if len(cell) > 0:
            size_column = cell[2].get_text(strip=True)
            size.append(size_column)

    # Find all 'td' elements in the 1st (0) column
    for row in soup.find_all('tr'):
        cell = row.find_all('td')
        if len(cell) > 0:
            time_column = cell[0].get_text(strip=True)
            time.append(time_column)

    # Pair each location with its corresponding world number
    data = list(zip(worlds, locations, size, time))

    # sizes and times to filter collected data by
    wanted_sizes = {'T6', 'T7', 'T8', 'T9'}
    wanted_times = {'0m ago', '1m ago', '2m ago', '3m ago', '4m ago', '5m ago'}

    filtered_data = [item for item in data if item[2] in wanted_sizes and item[3] in wanted_times]

    # Present data on console
    for item in filtered_data:
        print(item)

url = "https://osrsportal.com/shooting-stars-tracker"

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

try:
    while True:
        scrape_data(driver)
        # Wait for N seconds
        time.sleep(30)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()