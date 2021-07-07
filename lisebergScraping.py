from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import requests
from time import sleep
import config

def scrap_data(site, driver):
    driver.get(site)
    
    sleep(8)
    
    d = driver.find_elements_by_class_name('date-picker__button')[0].click()
    
    sleep(4)
    text_field = driver.find_elements_by_class_name('DayPicker__focus-region')
    if(len(text_field)):

        return text_field[0].text
    else:
        return None
    

def parse_data(data_list):
    avaliable = []
    all_days = data_list.split("\n")
    all_days = all_days[7:]
    

    it = iter(all_days)
    next(it)
    for i in all_days:
        try:
            k = next(it)
            if (k != "Fullt*" and i != "Fullt*" and i != "1"):
                print(i)
                avaliable.append(i)
        except:
            pass
    return avaliable


def send_to_discord(avaliable_days):
    if len(avaliable_days) > 0:
        data = {"content": "go go go book now! there is one" + str(avaliable_days)}
        response = requests.post(config.discord_url, data)
        print(avaliable_days)

    else:
        data = {"content": "Test, sent by python: " + str(avaliable_days)}
#        response = requests.post(config.discord_url, data)
        print(avaliable_days)




if __name__ == "__main__":
    print("Starting")
    print(config.discord_url)

    url = "https://www.liseberg.se/biljetter-priser/"


    webDriver = webdriver.Firefox()

    counter = 0
    while True:
        data = scrap_data(url, webDriver)
        if data is not None:
            avaliable_days = parse_data(data)
            send_to_discord(avaliable_days)
            counter+= 1
            print("Counter: ", counter)

        sleep(60*15)
        webDriver.refresh();


