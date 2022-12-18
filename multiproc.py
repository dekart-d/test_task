#На сайте есть функция, если кликаешь в любую точку сайта и переходишь в браузере на предыдущую страницу,
#срабатывает скрипт, который тебя редиректит на партнёрскую ссылку
#Цель этого скрипта проверить корректность распределения трафика между различными партнёрскими ссылками
from datetime import datetime
from multiprocessing import Process, Manager
from selenium import webdriver
from selenium.webdriver.common.by import By
from multiprocessing import Pool




NUM_OF_OPEN = 100
NUM_OF_PROCESSES = 20
options = webdriver.ChromeOptions()
options.headless = True
site = 'ссылка на проект'
def open_site(d):
    for i in range(int(NUM_OF_OPEN/NUM_OF_PROCESSES)):
        driver = get_driver()
        is_loading = True
        step = None
        while is_loading:
            step = driver.current_url.replace('https://', '').replace('www.', '').partition('/')[0]
            if step != 'data:,':
                is_loading = False
            else:
                driver = get_driver()
                #print(step)
        if step not in d:
            d[step] = 0
        d[step] += 1
        if i % int((NUM_OF_OPEN/NUM_OF_PROCESSES)/3) == 0:
            print(d)
        driver.quit()

def get_driver():
    driver = webdriver.Chrome(options=options)
    driver.delete_all_cookies()
    driver.get(site)
    driver.find_element(By.XPATH, '/html/body/div[4]/section[5]/div/h2').click()
    driver.back()
    return driver


if __name__ == '__main__':
    start_time = datetime.now()
    p = Pool(NUM_OF_PROCESSES)
    manager = Manager()
    d = manager.dict({})
    for _ in range(NUM_OF_PROCESSES):
        p.apply_async(open_site, args=(d,))
    p.close()
    p.join()
    print(f'Number of cycle - {NUM_OF_OPEN}')
    print(f'Site - {site}')
    for key, value in d.items():
        percent = (value / NUM_OF_OPEN) * 100
        print(f'{key}: {value} - {(percent)} %')
    print(datetime.now() - start_time)


