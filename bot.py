from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import html
import tweepy
from datetime import datetime as dt

'''
NOTAS

Criar executável: pyinstaller --clean -F bot.py
'''


'''
FUNCTIONS
'''


def open_browser():
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
    # Twitter authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)

    api = tweepy.API(auth)
    api.update_status(msg)
    print(f'Tweet enviado às {dt.now()}:\n{msg}')
    return


def read_keys(file):
    try:
        f = open(file, 'rb')
    except FileNotFoundError:
        raise FileNotFoundError("O arquivo com as chaves não foi encontrado.")

    keys_file = f.read().decode('UTF-8').splitlines()
    f.close()

    keys = []
    sep = ' = '
    for key in keys_file:
        keys.append(key[key.find(sep)+len(sep)+1:-1])
    return keys


def find_next_post_hour_index(post_hours):
    hour_now = dt.now().hour
    try:
        next_index = next(index for index, hour in enumerate(
            post_hours) if hour >= hour_now)
    except StopIteration:
        next_index = 0
    finally:
        return next_index


def countdown(n, step, text_plural, text_singular):
    while n > 0:
        count_plural = text_plural.format(n)
        count_singular = text_singular.format(n)

        if n > 1:
            print(count_plural, end='\r')
        elif n == 1:
            print(count_singular, end='\r')
        else:
            print('Contagem regressiva com número negativo.')
            input('Pressione ENTER para finalizar.')
            exit()

        n -= step
        sleep(step)
        print(' ' * max(len(count_plural), len(count_singular)), end='\r')


'''
MAIN
'''


def main():
    driver = open_browser()
    wdw = WebDriverWait(driver, 15, poll_frequency=0.5,
                        ignored_exceptions=None)
    url = 'http://www.quantocustaobrasil.com.br/2012/widget_300x220_txt/'

    keys = read_keys('keys.txt')
    post_hours = [7, 12, 20]
    next_post_hour_index = find_next_post_hour_index(post_hours)

    while True:
        if dt.now().hour == post_hours[next_post_hour_index]:
            text = get_msg(driver, url, wdw)
            send_msg(keys[0], keys[1], keys[2], keys[3], text)
            next_post_hour_index += 1
            if next_post_hour_index >= len(post_hours):
                next_post_hour_index = 0
        else:
            print(
                f'Próximo envio às {post_hours[next_post_hour_index]}h. {dt.now()}')

        countdown(15*60, 10, 'Nova tentativa em {} segundos.',
                  'Nova tentativa em {} segundo.')


if __name__ == '__main__':
    main()
