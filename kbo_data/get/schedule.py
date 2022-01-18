import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
from bs4 import BeautifulSoup as bs
from kbo_data.get.util import change_name_to_id

def transform_date(year,month,day):
    if len(day) == 1:
        return str(year+month+"0"+day)
    else:
        return str(year+month+day)

# month는 2자리 수로 맞춰야 한다.
def get_schedule(year, month):
    """각 월마다 경기 스케쥴을 가져오는 함수
    예시) 
    > get_ schedule(year, month)
        status year month day away  home
        0	OK	2001  04	5	LG	   SK
        1	OK	2001  04	5	KIA	   두산
        2	OK	2001  04	5	롯데	현대
        3	OK	2001  04	5	한화    삼성
    ...	...	...	...	...	...	...
        82	OK  2001  04	28  삼성	현대
        83	OK  2001  04	28	LG	   한화
    """
    with requests.Session() as s:
        r = s.get('https://www.koreabaseball.com/ws/Schedule.asmx/GetMonthSchedule', verify=False)
        data = {
            'leId': '1'
            ,'srIdList': ''
            , 'seasonId': year
            , 'gameMonth': month
        }
        r = requests.post('https://www.koreabaseball.com/ws/Schedule.asmx/GetMonthSchedule',  data=data)
        soup = bs(r.content, 'lxml')
        lists = soup.find_all("li")
        data=[]
        for lis in lists:
            temp= lis.text.split()
            if len(temp) == 5:
                data.append(["OK",transform_date(year,month,day),change_name_to_id(temp[0],year),change_name_to_id(temp[-1],year)])
            elif lis["class"]== ['\\"dayNum\\"']:
                day = lis.string
            elif lis["class"]== ['rainCancel']:
                data.append(["rain",transform_date(year,month,day),change_name_to_id(temp[0],year),change_name_to_id(temp[-1],year)])
            else:
                pass
        result = pd.DataFrame(data,columns=["status","date","away","home"])
    return result

def add_gameid():
    """
    ex) add_gameid()
        date	away	home	gameid
    0	20210501	SK	OB	SKOB0
    1	20210501	HH	LT	HHLT0
    2	20210501	LG	SS	LGSS0
    3	20210501	WO	NC	WONC0
    4	20210501	HT	KT	HTKT0
    ...	...	...	...	...
    108	20210530	WO	LG	WOLG0
    """