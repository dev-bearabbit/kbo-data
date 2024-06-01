"""KBO 정규 시즌 게임 자료를 가져와서 사용할 수 있도록 가공하기 쉽게 수정해주는 모듈 
"""
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from kbodata.parser.batter import batter_modify
from tqdm import tqdm
from kbodata.parser.page import parsing_single_game, is_game_finished
from kbodata.parser.scoreboard import scoreboard_modify
from kbodata.parser.batter import batter_modify
from kbodata.parser.pitcher import pitcher_modify
 
def get_single_game_data(date, gameId, driver):
    """단일 경기 데이터를 크롤링하고 사용할 데이터로 전처리 해주는 함수
    """
    raw_data = parsing_single_game(date, gameId, driver)
    scoreboard_modify(raw_data)
    batter_modify(raw_data)
    pitcher_modify(raw_data)
    return raw_data

def get_game_data(schedule, Driver_path):
    """스케쥴에 해당하는 데이터를 가져오는 함수
    데이터들을 스크래핑하여 list로 반환한다.
    """
    data = []
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")
    options.add_argument("--log-level=2")
    driver = webdriver.Chrome(service=Service(executable_path=Driver_path) , options=options)
    driver.implicitly_wait(100)

    today = date.today().strftime("%Y%m%d")
    today_result = is_game_finished(today, driver)

    with tqdm(desc="in progress",total=len(schedule)) as pbar:
        for idx, row in schedule.iterrows():
            # 취소된 경기나 미래 날짜의 경기는 제외
            if (row["status"] == 'canceled') or (row["status"]== 'scheduled'):
                pbar.update(1)
            # 오늘자 경기의 경우 종료되었는지 확인하고 크롤링
            elif row["status"] == 'ongoing':
                if today_result[row["gameid"]] == 1:
                    result = get_single_game_data(row["date"],row["gameid"],driver)
                    data.append(result)
                    pbar.update(1)
                else:
                    pbar.update(1)
                    continue
            # 끝난 경기라면 바로 크롤링
            else:
                result = get_single_game_data(row["date"],row["gameid"],driver)
                data.append(result)
                pbar.update(1)
    driver.quit()
    return data

