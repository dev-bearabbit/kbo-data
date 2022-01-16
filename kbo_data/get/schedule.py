import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import re
import lxml
import pandas as pd
from bs4 import BeautifulSoup as bs
from datetime import datetime

# month는 2자리 수로 맞춰야 한다.
def get_schedule(year, month):
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
            if len(lis.text.split()) == 5:
                temp= lis.text.split()
                data.append(["OK",year,month,day,temp[0],temp[-1]])
            elif lis["class"]== ['\\"dayNum\\"']:
                day = lis.string
            elif lis["class"]== ['rainCancel']:
                data.append(["rain",year,month,day,temp[0],temp[2]])
            else:
                pass
        result = pd.DataFrame(data,columns=["status","year","month","day","away","home"])
    return result
