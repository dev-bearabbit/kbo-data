
from datetime import date
import os
import configparser
from tqdm import tqdm
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta
from selenium import webdriver
import pandas as pd
from kbodata.get.util import change_name_to_id

# 설정파일을 읽어오기 위해 configparser를 사용
config = configparser.ConfigParser()
# 필요한 변수 가져오기
config.read(os.path.join(os.path.dirname('__file__'),"kbodata","config","config.ini"), encoding="utf-8")
info_url = config["DEFAULT"]["Game_info_URL"]


def get_schedule(start_date, end_date, Driver_path, only_month = False):
    """실제 사용하는 함수: 2008년부터 달 단위로 요청된 경기 스케쥴을 가져온다.

    ex) get_schedule("202104","202105",'chromedriver')

        status      date home away  dbheader gameid
    0     경기취소  20210403   HH   KT         0  HHKT0
    1     경기취소  20210403   HT   OB         0  HTOB0
    ..     ...       ...  ...  ...       ...    ...
    259     종료  20210530   KT   HT         0  KTHT0
    260     종료  20210530   NC   LT         0  NCLT0
    """
    if len(start_date+end_date) != 12 or (start_date+end_date).isdigit() == False:
        return print("ERROR: please check start date or end date")
    schedule = pd.DataFrame()
    st_date = date(int(start_date[:4]),int(start_date[4:7]),1)
    ed_date = date(int(end_date[:4]),int(end_date[4:7]),2)
    
    if st_date.year < 2008: return print("ERROR: This library only provides data since 2008.")
    if st_date >= ed_date: return print("ERROR: start date is later than the end date.")
    if ed_date > date.today(): return print("ERROR: The end date is later than now.")
    
    delta = relativedelta(ed_date, st_date)
    
    if only_month == True:
        if st_date.month != ed_date.month: return print("ERROR: start and end months are different")
        with tqdm(desc="in progress",total=delta.years+1) as pbar:
            while st_date.year <= ed_date.year:
                data = get_monthly_schedule(st_date.year,st_date.month,Driver_path)
                schedule = pd.concat([schedule,data],axis=0,ignore_index=True)
                st_date += relativedelta(years=1)
                pbar.update(1)
    else:
        with tqdm(desc="in progress",total=delta.years*12+delta.months+1) as pbar:
            while st_date < ed_date:
                data = get_monthly_schedule(st_date.year,st_date.month,Driver_path)
                schedule = pd.concat([schedule,data],axis=0,ignore_index=True)
                st_date += relativedelta(months=1)
                pbar.update(1)
    return schedule


def get_monthly_schedule(year, month, Driver_path):

    try:
        # 스케쥴 데이터 스크래핑
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("window-size=1920x1080")
        options.add_argument("disable-gpu")
        driver = webdriver.Chrome(Driver_path, options=options)
        url = info_url + str(year)+str(month).zfill(2)
        driver.get(url)
        driver.implicitly_wait(5)
        # 스크래핑 된 데이터 정리
        soup = BeautifulSoup(driver.page_source, "lxml")
        table = soup.find('tbody',{"id":"scheduleList"})
        result = []
        for tr in table.find_all("tr"):
            # 경기가 없는 경우에도 저장 X
            if 'tr_empty' in tr['class']:
                continue
            # 경기가 올스타전(드림 vs.나눔)인 경우 저장 X
            if tr.find("td",{"class":"td_sort"}).text == '올스타전':
                continue
            status = tr.find("span",{"class":"state_game"}).text
            # 업데이트 안된 경기들도 저장 X
            if status == '경기전':
                continue
            day = tr['data-date']
            teams = tr.find("td",{"class":"td_team"})
                
            result.append(transform_info(status,day,teams))
        result = pd.DataFrame(result, columns=["status","date","home","away"])
        result["status"].replace("경기취소", "canceled", inplace=True)
        result["status"].replace("종료", "finished", inplace=True)
        result = add_gameid(result)
    except Exception as e:
        print()
    return result


def transform_info(status, day, teams):
    """팀 정보를 가져오는 함수. HTML에 있는 요소들을 찾아서 하나의 리스트로 업로드한다.
        ex) html 코드 -> []
    """
    home = teams.find("div",{"class":"info_team team_home"})
    home_team = home.find("span",{"class":"txt_team"}).text
    away = teams.find("div",{"class":"info_team team_away"})
    away_team = away.find("span",{"class":"txt_team"}).text
    return [status, day, change_name_to_id(home_team,day[:4]), change_name_to_id(away_team,day[:4])]


def add_gameid(result):
    """gameid를 생성한다.  gameid는 (away+home+dbheader)로 구성된 문자열이다.
       더블헤더를 확인하는 기준은 다음과 같다.  더블헤더 x: 0 / 더블헤더 o: 1(첫번째 경기), 2(두번째 경기)
    """
    # 더블헤더 여부 저장할 열 생성
    result["dbheader"] = 0
    # 날짜 별 경기 횟수 조회
    temp = result.groupby(["status","date","away","home"],as_index=False).count()
    # 그 중 더블헤더 경기만 추출
    dbheader = temp.loc[temp["dbheader"] == 2]
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
    result["gameid"] = result[["home","away","dbheader"]].apply(lambda row: ''.join(row.values.astype(str)), axis=1)

    return result