from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import time
import os
import shutil
import re
import pandas as pd

directory=r'<저장될 경로>'
options = webdriver.ChromeOptions()
############
# 창이 뜨지 않게 설정
options.add_argument('headless')
# 창 크기 조절 설정
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
# F11 전체 화면 설정
options.add_argument('--start-fullscreen')
############
#지정한 user-agent로 설정합니다.
user_agent = "Mozilla/5.0 (Linux; Android 9; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.83 Mobile Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument('headless') #headless모드 브라우저가 뜨지 않고 실행됩니다.
options.add_argument('--window-size= x, y') #실행되는 브라우저 크기를 지정할 수 있습니다.
options.add_argument('--start-maximized') #브라우저가 최대화된 상태로 실행됩니다.
options.add_argument('--start-fullscreen') #브라우저가 풀스크린 모드(F11)로 실행됩니다.
options.add_argument('--blink-settings=imagesEnabled=false') #브라우저에서 이미지 로딩을 하지 않습니다.
options.add_argument('--mute-audio') #브라우저에 음소거 옵션을 적용합니다.
options.add_argument('incognito') #시크릿 모드의 브라우저가 실행됩니다.

###############
# 기본 다운로드 경로 설정 /쓰지 말고 \\로 사용할 것.
options.add_experimental_option("prefs", {
  "download.default_directory": directory,
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})



#웹 열기
driver = webdriver.Chrome(executable_path='c:/selenium/chromedriver', chrome_options=options)

#될때까지 기다리게하기
wait= WebDriverWait(driver, 10)
temp2=wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input#ststistic_period")))

#alert 팝업 확인하기
Alert(driver).text
#case 1
alert = driver.switch_to.alert
alert.accept()
#case 2
Alert(driver).accept()

#iframe 이동하기
# 상위로 이동
driver.switch_to.default_content()
driver.switch_to.frame(<iframe name>)

#iframe은 아닌데 비슷한게 있는듯.( 예 : chrome download)
shadow_root = driver.execute_script('return arguments[0].shadowRoot', <element>)

#select 버튼에 값 입력
Select(driver.find_element_by_css_selector(<CSS>)).select_by_value(<value>)

#캡처
driver.get_screenshot_as_file('<파일명>.png')

#driver 내에 열린 창 목록 가져오기
main=driver.window_handles[0]
#사용중인 창 바꾸기
driver.switch_to.window(driver.window_handles[pop])

#자바스크립트 보내기
driver.execute_script('$javascript:doSelect();')

#요소로 마우스 이동시키기
action=ActionChains(driver)
action.move_to_element(mainmenu)