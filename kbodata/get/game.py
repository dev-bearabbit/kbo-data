"""KBO 정규 시즌 게임 자료를 가져와서 사용할 수 있도록 가공하기 쉽게 수정해주는 모듈 
"""
from selenium import webdriver
from tqdm import tqdm
from kbodata.parser.page import parsing_single_game


def get_game_data(schedule, Driver_path):
    """스케쥴에 해당하는 데이터를 가져오는 함수
    데이터들을 스크래핑하여 list로 반환한다.
    """
    data = []
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")
    # 혹은 options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(Driver_path, options=options)
    driver.implicitly_wait(100)

    with tqdm(desc="in progress",total=len(schedule)) as pbar:
        for idx, row in schedule.iterrows():
            if row["status"] == 'canceled':
                pbar.update(1)
            else:
                raw_data = parsing_single_game(row["date"],row["gameid"],driver)
                data.append(raw_data)
                pbar.update(1)
    driver.quit()
    return data
