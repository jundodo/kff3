from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))

titles = []
sources = []
contents = []
facts = []
links = []
last_reg_dates=[]
current_address = []

def select_date():
    select_date_element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/select')
    select = Select(select_date_element)
    select.select_by_index(0)
    selected_option_text = select.first_selected_option.text
    last_date = selected_option_text.replace("최종 등록: ","").strip()
    return last_date

#기사 개수 1부터 시작
article_amount = int(input("원하는 기사 개수를 입력하세요 : "))

for i in range(1,article_amount+1):
    
    #출처 links 가져오기 위함
    all_links = []

    #해당 url로 이동
    url = f"https://factcheck.snu.ac.kr/facts/show?id={i}"
    driver.get(url)
    driver.implicitly_wait(10)
    
    #title, fact 없다면 다음 페이지로
    try:
        title = driver.find_element(By.CSS_SELECTOR, '.jsx-727853492 .fact-lead-message').text
        fact = driver.find_element(By.CSS_SELECTOR, '.jsx-727853492 .fact-dial-label-text').text
    except NoSuchElementException:
        continue
    
    #fact 부분 없어도 none으로 두고 싶다면 해당 코드로
    # try:
    #     fact = driver.find_element(By.CSS_SELECTOR, '.jsx-727853492 .fact-dial-label-text').text
    # except NoSuchElementException:
    #     fact = None
    
    source = driver.find_element(By.CSS_SELECTOR, '.jsx-727853492 .fact-check-source').text
        
    content = driver.find_element(By.CSS_SELECTOR, '.jsx-727853492 .mobile-display').text
    
    try:
        last_reg_date = select_date()
    except NoSuchElementException:
        last_reg_date = None

    current_url = driver.current_url
        #해당 url의 내용 스크랩핑
    
    source_links = driver.find_elements(By.CSS_SELECTOR, '.jsx-727853492 .fact-check-source .jsx-727853492')
    #모든 source_link 가져오기 위함
    
    # 웹 요소가 없으면 '-'를 추가
    if not source_links:
        source_links.append('-')

    for link in source_links:
        # '-' 문자열이면 그대로 '-', 아니면 href 속성을 가져옴
        if link == '-':
            get_link = '-'
            all_links.append(get_link)
        else:
            get_link = link.get_attribute('href')
            all_links.append(get_link)

    driver.implicitly_wait(10)

    titles.append(title)
    sources.append(source)
    contents.append(content)
    facts.append(fact)
    last_reg_dates.append(last_reg_date)
    current_address.append(current_url)
    links.append(all_links)
driver.quit()

df = pd.DataFrame({
    'Title' : titles,
    'Source' : sources,
    'Content' : contents,
    'Fact' : facts,
    'last register date' : last_reg_dates,
    'Source links' : links,
    'Snu url' : current_address
})
df.to_excel('/Users/home/Desktop/recentVision/crawled_snu_data.xlsx',index = False)