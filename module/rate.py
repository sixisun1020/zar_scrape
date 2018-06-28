from bs4 import BeautifulSoup
import datetime
from psycopg2 import connect
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def rate_scraping():
    options = Options()
    options.set_headless(True)
    driver = webdriver.Chrome(executable_path=r"C:/Users/cw/Documents/workspace/chromedriver.exe",chrome_options=options)

    host = 'localhost'
    port = '5432'
    user = 'postgres'
    password = 'postgres'
    database = 'zar_com'

    global dmm_rate
    global click_rate

    date_format = "%Y-%m-%d"

    conn = connect(host=host, port=port, user=user, password=password, database=database)
    c = conn.cursor()


    today = datetime.datetime.today()

    try:
        '''DMMFXの為替レート(Bid)'''
        url = "https://fx.dmm.com/market/rate/"
        driver.get(url)
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "html.parser")

        dmm_tag = "#ZARJPY_BID"
        dmm_ = soup.select_one(dmm_tag).contents
        dmm_rate = [float(rate) for rate in dmm_][0]

    except: 
        pass

    url = 'https://www.click365.jp/market.html'
    driver.get(url)


    try:
        '''Click365の為替レート(ASK)'''
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        click_tag = "#fx_api01 > tr:nth-of-type(8) > td:nth-of-type(3)"
        click_ = soup.select_one(click_tag).contents
    
        if re.compile(r'img').search(str(click_[0])):
            click_rate = float(click_[1])
        else:
            click_rate = float(click_[0])

    except: 
        print('something error.')
        pass

    if dmm_rate and click_rate:
        try:
            today = today.strftime(date_format)
            print('DMM:{}  CLICK:{}'.format(dmm_rate, click_rate))
            c.execute("insert into rate (write_date, dmm_rate, click_rate) values ('{}', {}, {});".format(today, dmm_rate, click_rate))
            print("insert into rate (write_date, dmm_rate, click_rate) values ('{}', {}, {});".format(today, dmm_rate, click_rate))
            conn.commit()
        except:
            pass
        
    driver.close()
    driver.quit()
    c.close()
    conn.close()
    print('rate Data is scraped.')
