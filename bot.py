from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import html
import tweepy
from datetime import datetime


'''
FUNCTIONS
'''

def open_browser(driver):
    profile = webdriver.FirefoxProfile()
    profile.set_preference('intl.accept_languages', 'en')
    options = webdriver.FirefoxOptions()
    options.headless = True
    return webdriver.Firefox(firefox_profile=profile, options=options)


def get_value(driver, el_id):
    element = driver.find_element_by_id(el_id)
    value = html.unescape(element.get_attribute('innerHTML'))
    return value


def get_msg(driver, url, wdw):
    driver.get(url)
    wdw.until(presence_of_element_located((By.ID, 'cont')))
    sleep(1)
    title = get_value(driver, 'titulo')
    value = get_value(driver, 'cont')
    msg = f'Este é o roubo que a sonegação de impostos evitou {title.split(", ")[1]}:\n\n{value}'
    return msg


def send_msg(consumer_key, consumer_secret, key, secret, msg):
    #Twitter authentication
    consumer_key = '123zKkQFrW6ia1cWQWzHalYzy'
    consumer_secret = 'ZTH9mg82M6KdPFG4XwK1a7IbAzzwCAg9ZF5x8qQSfUkW2MPq4v'
    key = '1312168239724625920-glxwhYBiMeh2cgpvuKwGgaCUtv3ziW'
    secret = 'qVlIcbqAMeMyR3agQFnISTru5swQjCNH7gRevPXdLHnew'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)

    api = tweepy.API(auth)
    api.update_status(msg)
    print(f'Tweet enviado às {datetime.now()}:\n{msg}')
    return


'''
MAIN
'''

def main():
    driver = open_browser('geckodriver.exe')
    wdw = WebDriverWait(driver, 15, poll_frequency=0.5, ignored_exceptions=None)
    url = 'http://www.quantocustaobrasil.com.br/2012/widget_300x220_txt/'
    consumer_key = '123zKkQFrW6ia1cWQWzHalYzy'
    consumer_secret = 'ZTH9mg82M6KdPFG4XwK1a7IbAzzwCAg9ZF5x8qQSfUkW2MPq4v'
    key = '1312168239724625920-glxwhYBiMeh2cgpvuKwGgaCUtv3ziW'
    secret = 'qVlIcbqAMeMyR3agQFnISTru5swQjCNH7gRevPXdLHnew'
    
    while True:
        text = get_msg(driver, url, wdw)
        send_msg(consumer_key, consumer_secret, key, secret, text)
        sleep(int(8*60*60))


if __name__ == '__main__':
    main()