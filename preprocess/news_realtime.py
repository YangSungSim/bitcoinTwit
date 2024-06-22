# news realtime google

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
from pymongo import MongoClient

driver = webdriver.Chrome()
driver.get('https://www.google.com/finance/')
driver.implicitly_wait(1)


def click_and_collect_news(driver, button_xpath, news_list, type):
    # 버튼 클릭
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, button_xpath))
    )
    submit_button.click()
    driver.implicitly_wait(30)

    path = '#yDmH0d > c-wiz.zQTmif.SSPGKf.ccEnac > div > div.e1AOyf > div > div > div.fAThCb > c-wiz:nth-child(2) > section > div:nth-child(2) > div > div'
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, path))
    )
    time.sleep(5)
    # 뉴스 데이터 추출 경로
    
    data = driver.find_elements(by=By.CSS_SELECTOR, value=path)
    
    num = len(data)
    for news_index in range(2, num):
        detail_path = f'#yDmH0d > c-wiz.zQTmif.SSPGKf.ccEnac > div > div.e1AOyf > div > div > div.fAThCb > c-wiz:nth-child(2) > section > div:nth-child(2) > div > div:nth-child({news_index}) > div > div.z4rs2b > a > div > div.Yfwt5'
        text_resource = driver.find_element(by=By.CSS_SELECTOR, value=detail_path)
        news_text = text_resource.text
        news_list.append([type, news_text])



def execute():
    news = []

    # 주요 뉴스
    click_and_collect_news(driver, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[4]/div/div/div[1]/c-wiz[2]/section/div[2]/div/div[1]/div/div/div/div/div[1]', news, 'hot_line')

    # 국내 주식 시장
    click_and_collect_news(driver, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[4]/div/div/div[1]/c-wiz[2]/section/div[2]/div/div[1]/div/div/div/div/div[2]', news, 'domestic')

    # 해외 주식 시장
    click_and_collect_news(driver, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[4]/div/div/div[1]/c-wiz[2]/section/div[2]/div/div[1]/div/div/div/div/div[3]', news, 'abroad')


    # save logic
    print(news)

    client = MongoClient('mongodb://root:password@localhost:27017/')
    db = client['news_database']

    news_post = db['newsdb']

    for type, text in news:
        post = {
            "date": datetime.datetime.now(tz=datetime.timezone.utc),
            "type": type,
            "headline": text
        }

        news_post.insert_one(post)

if __name__ == "__main__":
    execute()