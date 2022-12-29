# -*- coding: utf-8 -*-

import logging
import logging.handlers
import json
import getpass
import time
import datetime as dt
import pandas as pd

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup


logger = logging.getLogger('scraping_main')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.handlers.RotatingFileHandler('scraping_main.log', maxBytes=104857, backupCount=3)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handler to logger
logger.addHandler(fh)
logger.addHandler(ch)

now_dt = dt.datetime.now()


def selenium_naver_login(naver_id, naver_pw):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(5)

    # 로그인 전용 화면
    # driver.get('https://nid.naver.com/nidlogin.login?svctype=262144&url=http://m.naver.com/aside/')
    naver_url = "http://naver.com"
    driver.get(naver_url)
    # # 아이디와 비밀번호 입력
    # driver.find_element_by_name('id').send_keys('ggtt7')
    # driver.find_element_by_name('pw').send_keys(pword)
    # # 로그인 버튼 클릭
    # driver.find_element_by_css_selector('#frmNIDLogin > fieldset > input').click()
    login_button = driver.find_element_by_css_selector(".link_login")
    login_button.click()

    # 아이디와 비밀번호 입력
    driver.execute_script(f"document.getElementsByName('id')[0].value='{naver_id}'")
    driver.execute_script(f"document.getElementsByName('pw')[0].value='{naver_pw}'")
    # 로그인 버튼 클릭
    driver.find_element_by_css_selector("#frmNIDLogin > fieldset > input").click()

    time.sleep(3)
    return driver


def scraping_board_list(driver, startdate=now_dt, enddate=now_dt, max_page_num=100):
    # target_date = '20.01.03'
    target_date = startdate.strftime("%y.%m.%d")
    logger.info('target_date: %s' % target_date)
    base_url = 'https://m.cafe.naver.com/ca-fe/web/cafes/29798500/menus/29'

    driver.get(base_url)
    # driver.switch_to_frame('cafe_main')
    for page_num in range(1, max_page_num):
        # 더보기 버튼 50번 클릭
        # driver.find_element_by_xpath('//*[@id="btnNextList"]/a').click()
        driver.find_element_by_css_selector('.u_cbox_btn_more').click()
        # 로딩 시간이 있으므로 타이밍 맞추기 위해 sleep(0.5)
        time.sleep(0.5)
        article_list = driver.find_elements_by_class_name('board_box ')
        article_item = article_list[-1]
        tag_list = article_item.find_elements_by_tag_name('a')
        article_item_tag1 = tag_list[0]  # 타이틀 바
        user_area = article_item_tag1.find_element_by_class_name('user_area')
        time_text = user_area.find_element_by_class_name('time').text
        if time_text < target_date and len(time_text) > 6:
            break

    # href 속성을 찾아 url을 리스트로 저장
    article_list = driver.find_elements_by_class_name('board_box ')
    article_urls = list()

    for i in range(len(article_list)):
        article_item = article_list[i]
        tag_list = article_item.find_elements_by_tag_name('a')
        article_item_tag1 = tag_list[0]  # 타이틀 바
        href_url = article_item_tag1.get_attribute('href')
        article_item_tag_title = article_item_tag1.find_element_by_class_name('tit')
        title_text = article_item_tag_title.text
        user_area = article_item_tag1.find_element_by_class_name('user_area')
        nick_text = user_area.find_element_by_class_name('nick').text
        time_text = user_area.find_element_by_class_name('time').text
        no_text = user_area.find_element_by_class_name('no').text

        article_item_tag2 = tag_list[-1]  # 댓글 카운
        reply_num_text = article_item_tag2.find_element_by_class_name('num').text  # 댓글

        date_list = pd.date_range(startdate, enddate)
        target_date_list = [target_date.strftime('%y.%m.%d') for target_date in date_list]
        if time_text[:-1] in target_date_list:
            article_urls.append(href_url)
            logger.info("=======" * 10)
            logger.info(title_text)
            logger.info(href_url)
            logger.info("%s %s %s reply: %s" % (nick_text, time_text, no_text, reply_num_text))

    logger.info("=======" * 10)
    logger.info("article_urls num: %d" % len(article_urls))

    return article_urls


def scraping_article_content(driver, article_urls, startdate, enddate):
    res_list = list()
    for article_url in article_urls:
        article_id = article_url[67:72]
        # article_url = 'https://m.cafe.naver.com/ca-fe/web/cafes/29798500/articles/%s?fromList=true&menuId=29' % article_id
        driver.get(article_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # 게시글에서 제목 추출
        title = soup.select('h2.tit')[0].get_text()
        while title == 'undefined\n        ':
            driver.get(article_url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # 게시글에서 제목 추출
            title = soup.select('h2.tit')[0].get_text()
            time.sleep(0.5)

        author = soup.find_all('a', {"class": "nick"})[1].text
        view_num = soup.find('span', {'class': 'no font_l'}).text
        view_num = view_num[3:].replace(',', '')
        view_num = int(view_num)

        # 내용을 하나의 텍스트로 만든다. (띄어쓰기 단위)
        content = soup.select('#postContent')[0].text
        content = content.replace('\xa0', '\n')
        content = content.replace('투표는 표시되지 않습니다', '')
        # dict 형태로만들어 결과 list 에 저장
        res_list.append({'title': title, 'author':  author, 'view_num': view_num, 'content': content})
        logger.info("%s: %s, %s" %(article_id, author, title.replace('\n', '')))
        # time.sleep(1)

    startdate = startdate.strftime("%Y%m%d")
    enddate = enddate.strftime("%Y%m%d")
    df = pd.DataFrame(res_list)
    if startdate == enddate:
        df.to_csv('result_%s.csv' % enddate, sep='\t', index=False)
    else:
        df.to_csv('result_%s_%s.csv' % (startdate, enddate), sep='\t', index=False)


def main():
    import argparse

    strdate = now_dt.strftime("%Y%m%d")

    parser = argparse.ArgumentParser()
    parser.add_argument('startdate',
                        type=lambda s: dt.datetime.strptime(s, "%Y%m%d").strftime("%Y%m%d"),
                        default=strdate,
                        help="Start Date",
                        nargs='?'
                        )
    parser.add_argument('enddate',
                        type=lambda s: dt.datetime.strptime(s, "%Y%m%d").strftime("%Y%m%d"),
                        default='19000101',
                        help="End Date",
                        nargs='?'
                        )
    parser.add_argument('max_page_num',
                        type=int,
                        default=100,
                        help="Max board page num",
                        nargs='?'
                        )

    parser.add_argument("--auto", help="auto naver login", action="store_true")

    args = parser.parse_args()

    if args.enddate > strdate:
        logger.warning("End Date over Today")
        return
    elif args.startdate > strdate:
        logger.warning("Start Date over Today")
        return
    elif args.enddate < args.startdate and args.enddate != '19000101':
        logger.warning("Start Date over End Date")
        return
    if args.enddate == '19000101' and args.startdate <= strdate:
        args.enddate = args.startdate

    logger.info("Start Date: %s" % args.startdate)
    logger.info("End Date: %s" % args.enddate)
    logger.info("Max Page Num: %d" % args.max_page_num)
    startdate = dt.datetime.strptime(args.startdate, "%Y%m%d")
    enddate = dt.datetime.strptime(args.enddate, "%Y%m%d")

    if not args.auto:
        naver_id = input('naver id: ')
        naver_pw = getpass.getpass('Enter pw:')
    else:
        with open(".config", "r") as f:
            auto_config = json.load(f)
            naver_id = auto_config['id']
            naver_pw = auto_config['pw']

    driver = selenium_naver_login(naver_id, naver_pw)
    article_urls = scraping_board_list(driver, startdate, enddate, args.max_page_num)
    scraping_article_content(driver, article_urls, startdate, enddate)


if __name__ == "__main__":
    main()
