from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import wget
from run_time import exec_time
import requests
video_data = []
os.chdir('D:/video')

@exec_time
def main():
    count = 0
    browser = webdriver.Chrome('./chromedriver')
    browser.get('https://www.pornhub.com/channels/public-agent/videos?o=da')
    login(browser)
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'showAllChanelVideos'))
    )
    while True:
        count += 1
        try:
            soup = BeautifulSoup(browser.page_source, 'lxml')
            for video in soup.select('#showAllChanelVideos')[0].select('.js-pop.videoblock'):
                video_data.append({
                    'title': video.select('.title')[0].text.strip(),
                    'url': 'https://www.pornhub.com' + video.select('.title')[0]('a')[0]['href']
                })
                title = video.select('.title')[0].text.strip()
                browser.find_element_by_link_text(title).click()
                downloadVideo(browser, title)
                browser.back()
            browser.find_element_by_css_selector('.page_next').click()
            print('page{} is done'.format(count))
        except Exception as e:
            print(e)
            print('完成')
            break
    browser.close()
    json_data = json.dumps(video_data, indent=4, sort_keys=True, ensure_ascii=False)
    with open('pornhub.json', 'a', encoding='utf-8') as f:
        f.write(json_data)


def downloadVideo(browser, title):
    video_resolution = []
    print('{} 下載中....'.format(title))
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'contentWrapper'))
    )
    soup = BeautifulSoup(browser.page_source, 'lxml')
    for download in soup.select('.downloadBtn.greyButton'):
        try:
            video_resolution.append(download['href'])
        except Exception:
            pass
    wget.download(video_resolution[0], out=title + '.mp4')


def login(browser):
    browser.find_element_by_id('headerLoginLink').click()
    browser.find_element_by_id('username').send_keys(input('Username: '))
    browser.find_element_by_id('password').send_keys(input('Password: '))
    browser.find_element_by_id('submit').click()
    browser.implicitly_wait(10)


if __name__ == '__main__':
    main()