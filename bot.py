from selenium.webdriver.support.ui import WebDriverWait
from functions import *
from keys import *

'''
NOTAS

Criar executável: pyinstaller --clean -F bot.py
'''


def main():

    driver = open_browser()
    wdw = WebDriverWait(driver, 15, poll_frequency=0.5,
                        ignored_exceptions=None)
    url = 'http://www.quantocustaobrasil.com.br/2012/widget_300x220_txt/'

    # keys = read_keys('keys.txt')
    post_hours = [7, 12, 20]
    next_post_hour_index = find_next_post_hour_index(post_hours)

    while True:
        if dt.now().hour == post_hours[next_post_hour_index]:
            text = get_msg(driver, url, wdw)
            send_msg(consumer_key, consumer_secret, key, secret, text)

            if next_post_hour_index < len(post_hours)-1:
                next_post_hour_index += 1
            else:
                next_post_hour_index = 0

        else:
            print(
                f'Próximo envio às {post_hours[next_post_hour_index]}h. {dt.now()}')

        countdown(15*60, 10, 'Nova tentativa em {} segundos.',
                  'Nova tentativa em {} segundo.')


if __name__ == '__main__':
    main()
