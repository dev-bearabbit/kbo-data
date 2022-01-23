
from datetime import date
from tqdm import tqdm
from dateutil.relativedelta import relativedelta
import pandas as pd
from kbodata.parser.schedule import parsing_daily_schedule, parsing_monthly_schedule


def get_daily(seleted_date, Driver_path):
    """유저 함수: 2008년 이후 데이터 중에 요청된 날짜의 경기 스케쥴을 가져온다.

    ex) get_daily_schedule("20210420","chromedriver")

        status      date home away  dbheader gameid
    0	finished	20210420	HT	LG	0	HTLG0
    1	finished	20210420	KT	NC	0	KTNC0
    2	finished	20210420	OB	LT	0	OBLT0
    3	finished	20210420	SK	SS	0	SKSS0
    4	finished	20210420	WO	HH	0	WOHH0
    """

    if len(seleted_date) != 8 or (seleted_date).isdigit() == False:
        return print("ERROR: please check start date or end date")

    sd_date = date(int(seleted_date[:4]),int(seleted_date[4:6]),int(seleted_date[6:8]))

    if sd_date.year < 2008: return print("ERROR: This library only provides data since 2008.")
    if sd_date > date.today(): return print("ERROR: The end date is later than now.")
    data = parsing_daily_schedule(seleted_date,Driver_path)
    return data


def get_monthly(start_date, end_date, Driver_path, only_month = False):
    """유저 함수: 2008년부터 달 단위로 요청된 경기 스케쥴을 가져온다.

    ex) get_monthly_schedule("202104","202105",'chromedriver')

        status      date home away  dbheader gameid
    0   canceled	20210403	HH	KT	0	HHKT0
    1	canceled	20210403	HT	OB	0	HTOB0
    2	canceled	20210403	LG	NC	0	LGNC0       
    ..     ...       ...  ...  ...       ...    ...
    262	finished	20210530	SK	HH	0	SKHH0
    263	finished	20210530	WO	LG	0	WOLG0
    """
    if len(start_date+end_date) != 12 or (start_date+end_date).isdigit() == False:
        return print("ERROR: please check start date or end date")
    schedule = pd.DataFrame()
    st_date = date(int(start_date[:4]),int(start_date[4:6]),1)
    ed_date = date(int(end_date[:4]),int(end_date[4:6]),2)
    
    if st_date.year < 2008: return print("ERROR: This library only provides data since 2008.")
    if st_date >= ed_date: return print("ERROR: start date is later than the end date.")
    if ed_date > date.today(): return print("ERROR: The end date is later than now.")
    
    delta = relativedelta(ed_date, st_date)
    
    if only_month == True:
        if st_date.month != ed_date.month: return print("ERROR: start and end months are different")
        with tqdm(desc="in progress",total=delta.years+1) as pbar:
            while st_date.year <= ed_date.year:
                data = parsing_monthly_schedule(st_date.year,st_date.month,Driver_path)
                schedule = pd.concat([schedule,data],axis=0,ignore_index=True)
                st_date += relativedelta(years=1)
                pbar.update(1)
    else:
        with tqdm(desc="in progress",total=delta.years*12+delta.months+1) as pbar:
            while st_date < ed_date:
                data = parsing_monthly_schedule(st_date.year,st_date.month,Driver_path)
                schedule = pd.concat([schedule,data],axis=0,ignore_index=True)
                st_date += relativedelta(months=1)
                pbar.update(1)
    return schedule
