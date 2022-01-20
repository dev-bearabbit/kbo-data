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
                data.append(["rain",transform_date(year,month,day),change_name_to_id(temp[0],year),change_name_to_id(temp[2],year)])
            else:
                pass
        result = pd.DataFrame(data,columns=["status","date","away","home"])
    return result

def add_gameid(result):
    """gameid를 생성한다.  gameid는 (away+home+dbheader)로 구성된 문자열이다.
       더블헤더를 확인하는 기준은 다음과 같다.  더블헤더 x: 0 / 더블헤더 o: 1(첫번째 경기), 2(두번째 경기)

    ex) add_gameid(data)
    status	date	  away	home  dbheader	gameid
    0	OK	20200602	SS	LG	   0	     SSLG0
    1	OK	20200602	SK	NC	   0	     SKNC0
    2	OK	20200602	OB	KT	   0	     OBKT0
    3	OK	20200602	LT	HT	   0	     LTHT0
    4	OK	20200602	WO	HH	   0	     WOHH0
        ...	...	...	...	...	...	...
    126	OK	20200630	KT	LG	   0	     KTLG0
    127	OK	20200630	SK	SS	   0	     SKSS0
    """
    # 더블헤더 여부 저장할 열 생성
    result["dbheader"] = 0
    # 날짜 별 경기 횟수 조회
    temp = result.groupby(["date","away","home"],as_index=False).count()
    # 그 중 더블헤더 경기만 추출
    dbheader = temp.loc[temp["status"] == 2]
    # 더블헤더 경기인 경우 1, 2 로 입력
    for idx, dbhd in dbheader.iterrows():
        bh = dbhd["date"]+dbhd["away"]+dbhd["home"]
        count = 1
        for jdx, data in result.iterrows():
            dt = data["date"]+data["away"]+data["home"]
            if dt == bh:
                result.iat[jdx, 4] = count
                count += 1
    # 더블헤더와 팀 정보로 gameid 생성
    result["gameid"] = result[["away","home","dbheader"]].apply(lambda row: ''.join(row.values.astype(str)), axis=1)

    return result

