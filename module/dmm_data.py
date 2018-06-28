from bs4 import BeautifulSoup
import datetime
from psycopg2 import connect
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def dmmSwap_scraping():

    #日付のデータ整形
    dateFormat = "%y-%m-%d"
    today = datetime.datetime.today()

    host = 'localhost'
    port = '5432'
    user = 'postgres'
    password = 'postgres'
    database = 'zar_com'
    num = 3

    def date_format(date_):
        month_day = date_.split('(').pop(0)
        date = str(today.year) + '/' + month_day

        return date
        

    options = Options()
    options.set_headless(True)

    driver = webdriver.Chrome(executable_path=r"C:/Users/cw/Documents/workspace/chromedriver.exe",chrome_options=options)

    try:
        driver.get("https://fx.dmm.com/market/swapcalendar_fx/index1.html")
    
        driver.find_element_by_id("swapbtn2").click()

        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "html.parser")


        tbody = soup.select_one("#table2 > tbody")
        td = tbody.find_all("td")

        conn = connect(host=host, port=port, database=database, user=user, password=password)
        c = conn.cursor()

        for tag in td:
            try:
                string_ = tag.get("class").pop(1)

                if "date" in string_:
                    date_ = tag.string
                    dateFormat = date_format(date_)

                    swap_tag = "#table2 > tbody > tr:nth-of-type(" + str(num) + ") > td:nth-of-type(5)"
                    swapData = soup.select_one(swap_tag).contents
                    try:
                        swap = list(map(int, swapData)).pop(0)
                    except:
                        swap = 0
                    c.execute("insert into dmms (write_date, swap) values ('{}', {});".format(dateFormat, swap))
                    conn.commit()
                    print("insert into dmms (write_date, swap) values ('{}', {});".format(dateFormat, swap))
                    num += 3   
            except:
                pass
    except:
        print('ERROR')
  

    c.close()
    conn.close()
    driver.close()

    driver.quit()
    print('dmmSwap data is scraped.')





