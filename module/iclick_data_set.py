import requests
from bs4 import BeautifulSoup
import datetime
from psycopg2 import connect
import time

def clickSwap_setup():
        
    host = 'localhost'
    port = '5432'
    user = 'postgres'
    password = 'postgres'
    database = 'zar_com'

    date_format = "%Y-%m-%d"
    today = datetime.datetime.today()


    conn = connect(host=host, port=port, user=user, password=password, database=database)
    c = conn.cursor()

    for i in range(1):
        year = 2018 + i

        for j in range (12):
            month = 1 + j
            time.sleep(1)
            try:
                url = "https://www.click-sec.com/corp/guide/c365/swplog/?year={}&month={:0>2}&pair=ZARJPY".format(year,month)
                html = requests.get(url)
                soup = BeautifulSoup(html.content, "html.parser")

                for i in range(31):
                    day = i+1

                    swap_tag = "#myForm > div.swap > table > tbody > tr:nth-of-type(" + str(day) + ") > td.col4.day"
                    dt = datetime.date(year, month, day)
                    dt_datetime =datetime.datetime(year,month,day)
                    swap_data = soup.select_one(swap_tag).text
                    write_date = dt.strftime(date_format)
                    if swap_data:
                        swap = int(swap_data)
                    else:
                        swap = 0
                    date_past = today - dt_datetime
                    if date_past.days >= 0:
                        c.execute("insert into clicks (write_date, swap) values ('{}', {});".format(write_date, swap))

            except:
                pass
    conn.commit()

    c.close()
    conn.close()
    print('setup is ready.')










