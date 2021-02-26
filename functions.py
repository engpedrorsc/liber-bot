from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from time import sleep
import html
import tweepy
from datetime import datetime as dt
import sys


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


def send_msg(driver, url, wdw, consumer_key, consumer_secret, key, secret):
    driver.get(url)
    wdw.until(presence_of_element_located((By.ID, 'cont')))
    sleep(1)
    title = get_value(driver, 'titulo')
    value = get_value(driver, 'cont')
    msg = f'Este é o roubo que a sonegação de impostos evitou {title.split(", ")[1]}:\n\n{value}'

    # Twitter authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)

    api = tweepy.API(auth)
    api.update_status(msg)
    print(f'Tweet enviado às {dt.now()}:\n{msg}')
    return


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
            sys.exit()

        n -= step
        sleep(step)
        print(' ' * max(len(count_plural), len(count_singular)), end='\r')


def increment(list, index):
    if index < len(list)-1:
        index += 1
    else:
        index = 0
    return index


def start_action(post_hours, next_post_hour_index, driver, url, wdw, consumer_key, consumer_secret, key, secret):
    list_of_choices = [1, 2, 3, 4]
    print(f'Próximo horário: {post_hours[next_post_hour_index]}h')
    print('1 - Postar a partir do próximo horário programado.')
    print('2 - Postar agora e PULAR o próximo horário programado.')
    print('3 - Postar agora e NÃO PULAR o próximo horário programado.')
    print('4 - Postar agora e FECHAR.')
    choice = int(input('\nDigite a sua opção e pressione ENTER: '))

    if choice not in list_of_choices:
        print('>>> Opção inválida. <<<\n')
        return start_action(post_hours, next_post_hour_index, driver, url, wdw, consumer_key, consumer_secret, key, secret)

    if choice == 1:
        pass
    elif choice == 2:
        send_msg(driver, url, wdw, consumer_key, consumer_secret, key, secret)
        next_post_hour_index = increment(post_hours, next_post_hour_index)
    elif choice == 3:
        send_msg(driver, url, wdw, consumer_key, consumer_secret, key, secret)
    elif choice == 4:
        send_msg(driver, url, wdw, consumer_key, consumer_secret, key, secret)
        input('Pressione ENTER para fechar.')
        sys.exit()

    return next_post_hour_index
