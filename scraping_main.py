
import time
import random
import requests

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from util.cmm_logger import *

logger = logging.getLogger('scraping_main')
logger.setLevel(logging.DEBUG)

# add the handler to logger
logger.addHandler(fh)
logger.addHandler(ch)

# agent 리스트 서버 이슈: https://domdom.tistory.com/329
# 버전업으로 해결 0.1 => 1.1
ua = UserAgent(verify_ssl=False)


def main(start_page=1, end_page=1):
    user_agent = ua.random
    logger.info(str(user_agent))

    options = Options()
    # options.headless = True
    options.add_argument("-private")
    options.set_preference("general.useragent.override", user_agent)
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(5)

    # naver_target_url = 'https://m.stock.naver.com/research/debenture'
    # driver.get(naver_target_url)
    #
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    # more_button = driver.find_element(By.CSS_SELECTOR, '.VMore_link__DAtli')
    # more_button.click()

    page_index = 1
    for page_index in range(start_page, end_page+1):
        logger.info('start downloading reports page: %d' % page_index)
        naver_page_url = 'https://finance.naver.com/research/debenture_list.naver?&page=' + '%d' % page_index
        driver.get(naver_page_url)

        target_table_body = driver.find_element(By.TAG_NAME, 'tbody')
        tr_list = target_table_body.find_elements(By.TAG_NAME, 'tr')

        # 게시물 리스트 LOOP
        for tr_item in tr_list:
            # tr_item = tr_list[2]
            td_list = tr_item.find_elements(By.TAG_NAME, 'td')
            # 게시물인 아닌경우 continue
            if len(td_list) != 5: continue

            target_name = ''
            for i in range(4):
                if i != 0 and i != 3:
                    target_name = target_name + '_' + td_list[i].text
                elif i == 3:
                    # 날짜
                    target_name = f'[{td_list[i].text}]_' + target_name
                else:
                    target_name = td_list[i].text

            td_item = td_list[2].find_element(By.TAG_NAME, 'a')
            target_link = td_item.get_attribute('href')
            target_name = target_name.replace('/', '').replace('..', '')
            target_name = target_name[:-1]

            logger.info(target_name)
            r = requests.get(target_link, allow_redirects=True)
            open('./pdf/' + target_name + '.pdf', 'wb').write(r.content)
            time.sleep(3 + random.uniform(0, 3))

    driver.quit()


if __name__ == "__main__":
    import argparse

    start_page = 1
    end_page = 1

    parser = argparse.ArgumentParser()
    parser.add_argument('start_page',
                        type=int,
                        default=start_page,
                        nargs='?')
    parser.add_argument('end_page',
                        type=int,
                        default=end_page,
                        nargs='?')

    args = parser.parse_args()

    main(args.start_page, args.end_page)
