from selenium.webdriver.support.ui import WebDriverWait
from functions import *
import os
import ast

'''
NOTAS

Criar executável: pyinstaller --clean -F bot.py
'''


def main():

    driver = open_browser()
    wdw = WebDriverWait(driver, 15, poll_frequency=0.5,
                        ignored_exceptions=None)
    url = os.getenv('SOURCE_URL')

    # keys = read_keys('keys.txt')
    post_hours = ast.literal_eval(os.getenv('POST_HOURS'))
    print(post_hours)
    next_post_hour_index = find_next_post_hour_index(post_hours)

    consumer_key = str(os.getenv('TWITTER_CONSUMER_KEY'))
    consumer_secret = str(os.getenv('TWITTER_CONSUMER_SECRET'))
    access_key = str(os.getenv('TWITTER_ACCESS_KEY'))
    access_secret = str(os.getenv('TWITTER_ACCESS_SECRET'))

    next_post_hour_index = start_action(
        post_hours, next_post_hour_index, driver, url, wdw, consumer_key, consumer_secret, access_key, access_secret)

    while True:
        if dt.now().hour == post_hours[next_post_hour_index]:
            send_msg(driver, url, wdw, consumer_key,
                     consumer_secret, access_key, access_secret)
            next_post_hour_index = increment(post_hours, next_post_hour_index)

        else:
            print(
                f'Próximo envio às {post_hours[next_post_hour_index]}h. {dt.now()}')

        countdown(15*60, 10, 'Nova tentativa em {} segundos.',
                  'Nova tentativa em {} segundo.')


if __name__ == '__main__':
    main()
