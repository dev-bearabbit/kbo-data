import os
import re
import configparser
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from kbodata.parser.util import change_name_to_id

# 설정파일을 읽어오기 위해 configparser를 사용
config = configparser.ConfigParser()
# 필요한 변수 가져오기
config.read(os.path.join(os.path.dirname(__file__),"config.ini"), encoding="utf-8")
info_url = config["DEFAULT"]["Game_info_URL"]


def parsing_monthly_schedule(year, month, driver):

    driver.get(info_url)

    # 페이지가 완전히 로드될 때까지 대기
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )
    try:
        year_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ddlYear")))
        year_element.send_keys(str(year)) 
        month_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ddlMonth")))
        month_element.send_keys(str(month).zfill(2))
    except TimeoutException:
        print("Unable to locate the element. The page may not have loaded completely.")

    data = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.ID,"tblSchedule")))
    # 스크래핑 된 데이터 정리
    table = BeautifulSoup(data.get_attribute('innerHTML'), "lxml")
    result = []
    not_listed = ["EAST", "WEST", "드림", "나눔"]
    for td in table.find_all("td"):
        # 경기 없는 날 확인
        if len(td) == 1:
            continue
        for li in td.find_all("li"):
            text = re.sub(r'\[.*?\]', '', li.text)
            info = (text).split()
            # 경기날짜 확인
            if li.get('class') == ['dayNum']:
                day = int(info[0].zfill(2))
                dt = str(year)+str(month).zfill(2) + info[0].zfill(2)
            # 나눔 경기는 제외
            elif info[0] in not_listed:
                continue
            # 경기 취소 확인
            elif (li.get('class') == ['rainCancel']) or (day == "20111025"):
                status = "canceled"
                home = change_name_to_id(info[2],year)
                away = change_name_to_id(info[0],year)
                result.append([status,dt,home,away])
            elif (len(info) < 5) & (date(year,month,day) == date.today()):
                status = "ongoing"
                home = change_name_to_id(info[-1],year)
                away = change_name_to_id(info[0],year)
                result.append([status,dt,home,away])
            elif (len(info) < 5) & (date(year,month,day) > date.today()):
                status = "scheduled"
                home = change_name_to_id(info[-1],year)
                away = change_name_to_id(info[0],year)
                result.append([status,dt,home,away])
            else:
                status = "finished"
                home = change_name_to_id(info[-1],year)
                away = change_name_to_id(info[0],year)
                result.append([status,dt,home,away])
    result = pd.DataFrame(result, columns=["status","date","home","away"])
    result = add_gameid(result)
    result = delete_non_provided_data(result)
    
    return result


def parsing_daily_schedule(year,month,day,driver):

    # 스케쥴 데이터 스크래핑
    driver.get(info_url)

    # 페이지가 완전히 로드될 때까지 대기
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )
    try:
        year_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ddlYear")))
        year_element.send_keys(str(year)) 
        month_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ddlMonth")))
        month_element.send_keys(str(month).zfill(2))
    except TimeoutException:
        print("Unable to locate the element. The page may not have loaded completely.")

    data = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.ID,"tblSchedule")))
    # 스크래핑 된 데이터 정리
    table= BeautifulSoup(data.get_attribute('innerHTML'), "lxml")
    result = []
    not_listed = ["EAST", "WEST", "드림", "나눔"]
    for td in table.find_all("td"):
        if td.find("li",{"class":"dayNum"}).text != str(day):
            continue
        for li in td.find_all("li"):
            text = re.sub(r'\[.*?\]', '', li.text)
            info = (text).split()
            # 경기날짜 확인
            if li.get('class') == ['dayNum']:
                dt = str(year)+str(month).zfill(2) + info[0].zfill(2)
            # 나눔 경기는 제외
            elif info[0] in not_listed:
                continue
            # 경기 취소 확인
            elif li.get('class') == ['rainCancel']:
                status = "canceled"
                home = change_name_to_id(info[2],year)
                away = change_name_to_id(info[0],year)
                result.append([status,dt,home,away])
            elif (len(info) < 5) & (date(year,month,day) == date.today()):
                status = "ongoing"
                home = change_name_to_id(info[-1],year)
                away = change_name_to_id(info[0],year)
                result.append([status,dt,home,away])
            elif (len(info) < 5) & (date(year,month,day) > date.today()):
                status = "scheduled"
                home = change_name_to_id(info[-1],year)
                away = change_name_to_id(info[0],year)
                result.append([status,dt,home,away])
            else:
                status = "finished"
                home = change_name_to_id(info[-1],year)
                away = change_name_to_id(info[0],year)
                result.append([status,dt,home,away])
    result = pd.DataFrame(result, columns=["status","date","home","away"])
    result = add_gameid(result)
    result = delete_non_provided_data(result)

    return result


def add_gameid(result):
    """gameid를 생성한다.  gameid는 (away+home+dbheader)로 구성된 문자열이다.
       더블헤더를 확인하는 기준은 다음과 같다.  더블헤더 x: 0 / 더블헤더 o: 1(첫번째 경기), 2(두번째 경기)
    """
    # 더블헤더 여부 저장할 열 생성
    result["dbheader"] = 0
    
    # 날짜 별 경기 횟수 조회
    temp = result.groupby(["date","away","home"],as_index=False).count()
    
    # 그 중 더블헤더 경기만 추출
    checker = temp.loc[temp["status"] == 2]
    
    # 더블헤더 중 첫 경기가 취소된 경기 제거
    dbheader = checker.copy()
    for idx, dbhd in dbheader.iterrows():
        bh = dbhd["date"]+dbhd["away"]+dbhd["home"]
        stat = list(result.loc[result["date"]+result["away"]+result["home"] == bh]["status"])
        if (stat[0] == 'canceled') & (stat[1] == 'finished'):
                dbheader = dbheader.drop(idx)
    
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

def delete_non_provided_data(result):
    """경기정보가 제공되지 않은 스케쥴을 제거하는 함수
    """
    not_provided = [("20080330","LTHH0"),
                    ("20090404","WOLT0"),
                    ("20100320","OBLT0"),
                    ("20100320","WOSS0"),
                    ("20150708","HTWO0"),
                    ("20180801","WOSK0")]
    for day, gameid in not_provided:
        idx = result[(result["date"]==day)&(result["gameid"]==gameid)].index
        result = result.drop(idx)
        result.reset_index(inplace=True,drop=True)

    not_provided_for_day = ["20130309",
                            "20130310",
                            "20130311",
                            "20130312",
                            "20130313",
                            "20130314",
                            "20130315",
                            "20130316",
                            "20130317",
                            "20130318",
                            "20130319",
                            "20130320",
                            ]
    for day in not_provided_for_day:
        idx = result[(result["date"]==day)].index
        result = result.drop(idx)
        result.reset_index(inplace=True,drop=True)

    return result
