from module.dmm_data import dmmSwap_scraping
from module.iclick_data import clickSwap_scraping
from module.rate import rate_scraping
from module.iclick_data_set import clickSwap_setup
from datetime import datetime
import time

clickSwap_setup()


now = datetime.now()
while True:
    if int(now.strftime('%H')) % 6 == 0:
        dmmSwap_scraping()
        clickSwap_scraping()
        rate_scraping()
        time.sleep(3600)
    



