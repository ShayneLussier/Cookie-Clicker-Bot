from selenium import webdriver
from selenium.webdriver.common.by import By
import time

session_length = float(input("How many minutes to you want to run the Cookie Clicker bot? (Enter an integer ex: 5 ) = "))
# ------------------------- SELENIUM SETUP -------------------------- #

# keep browser open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

# ------------------------- FUNCTIONS ------------------------- #

items = driver.find_elements(By.CSS_SELECTOR, '#store div')
item_ids = [item.get_attribute('id') for item in items]

def clickCookie(): # clicks the cookie for 5 seconds
    cookie = driver.find_element(By.ID, 'cookie')
    start_time = time.time()
    while (time.time() - start_time) < 5:
        cookie.click()
    buyStoreUpgrade()

def buyStoreUpgrade(): # purchases the highest cost available upgrade
    store = driver.find_elements(By.CSS_SELECTOR, '#store b')

    # list of all upgrade prices
    item_prices = []
    for prices in store:
        upgrade_info = prices.text
        if upgrade_info != "":
            cost = int(upgrade_info.split('-')[1].strip().replace(',', ""))
            item_prices.append(cost)

    # make dictionary = {15: 'buyCursor', ...}
    upgrades = {}
    for n in range(len(item_prices)):
        upgrades[item_prices[n]] = item_ids[n]

    affordable_upgrades = {}
    for cost, id in upgrades.items():
        if coinCount() > cost:
            affordable_upgrades[cost] = id

    highest_price_affordable_upgrade = max(affordable_upgrades)
    to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
    to_buy = driver.find_element(By.ID, to_purchase_id)
    to_buy.click() # click on highest affordable upgrade

def coinCount(): # returns coins
    coins = driver.find_element(By.ID, 'money')
    return int(coins.text)
        
# ------------------------- RUN GAME -------------------------- #

session_start = time.time()

while True:
    clickCookie()
    
    # Check session duration after each click
    if (time.time() - session_start) > session_length * 60:
        cookie_per_s = driver.find_element(By.ID, 'cps')
        print(cookie_per_s.text)
        break

driver.quit()