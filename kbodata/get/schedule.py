from datetime import date
from tqdm import tqdm
from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
from kbodata.parser.schedule import parsing_daily_schedule, parsing_monthly_schedule

def get_daily_schedule(year,month,day,Driver_path):
    """유저 함수: 2008년 이후 데이터 중에 요청된 날짜의 경기 스케쥴을 가져온다.

    ex) get_daily_schedule(2021,04,20,"chromedriver")

        status      date home away  dbheader gameid
    0	finished	20210420	HT	LG	0	HTLG0
    1	finished	20210420	KT	NC	0	KTNC0
    2	finished	20210420	OB	LT	0	OBLT0
    3	finished	20210420	SK	SS	0	SKSS0
    4	finished	20210420	WO	HH	0	WOHH0
    """

    if (str(year)+str(month)+str(day)).isdigit() == False:
        return print("ERROR: INVALID PARAMETER. please check year or month or day")

    sd_date = date(year, month, day)
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")
    options.add_argument("--log-level=2")
    driver = webdriver.Chrome(service=Service(executable_path=Driver_path) , options=options)
    driver.implicitly_wait(100)

    if sd_date.year < 2008: return print("ERROR: This library only provides data since 2008.")
    
    data = parsing_daily_schedule(year,month,day,driver)
    driver.quit()
    return data

def get_monthly_schedule(year, month, Driver_path):
    """유저 함수: 2008년부터 달 단위로 요청된 경기 스케쥴을 가져온다.
    """
    if (str(year)+str(month)).isdigit() == False:
        return print("ERROR: INVALID PARAMETER. please check year or month")
    st_date = date(year,month,1)
    
    if st_date.year < 2008: return print("ERROR: This library only provides data since 2008.")

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome(service=Service(executable_path=Driver_path) , options=options)
    driver.implicitly_wait(100)

    data = parsing_monthly_schedule(st_date.year,st_date.month,driver)
    driver.quit()

    return data

def get_yearly_schedule(year, Driver_path):
    """유저 함수: 2008년부터 년 단위로 요청된 경기 스케쥴을 가져온다.
    """
    if len(str(year)) != 4 or (str(year)).isdigit() == False:
        return print("ERROR: INVALID PARAMETER. please check year")
    schedule = pd.DataFrame()
    st_date = date(year,1,1)
    ed_date = date(year,12,30)
    
    if st_date.year < 2008: return print("ERROR: This library only provides data since 2008.")
    
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome(service=Service(executable_path=Driver_path) , options=options)
    driver.implicitly_wait(100)

    with tqdm(desc="in progress",total=12) as pbar:
        while st_date < ed_date:
            data = parsing_monthly_schedule(st_date.year,st_date.month,driver)
            schedule = pd.concat([schedule,data],axis=0,ignore_index=True)
            st_date += relativedelta(months=1)
            pbar.update(1)

    driver.quit()
    return schedule
