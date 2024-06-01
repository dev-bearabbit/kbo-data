import json
import os
import re
import configparser
import pandas as pd
from kbodata.parser.util import make_primary_key, get_game_info

# 설정파일을 읽어오기 위해 configparser를 사용
config = configparser.ConfigParser()
# 필요한 변수 가져오기
config.read(os.path.join(os.path.dirname(__file__),"config.ini"), encoding="utf-8")
Batter_factor = config["BATTER"]


def batter_modify(data):
    """수집한 여러 개의 경기가 들어 있는 자료에서 타자 자료만 정리하는 함수

    이 함수는 여러 경기자료(`data`)에서 스코어보드만 뽑아서 내용을 고치고 변경한 다음
    다시 원 자료(`data`)에 끼워 넣는다. 즉 반환 값에는 모든 수집한 내용이 들어 있다.
    참고로 아래 긴 `for`문은 18회까지 연장하기 위한 방법이다. 기본적으로 현재 정규 이닝은
    13회까지밖에 없지만, 예전 정규 KBO 리그에서 18회까지 있는 경우가 있어 이를 반영했다.

    Args:
        data (json): 수집한 하나 이상의 경기 자료

    Returns:
        data (json): 타자 자료만 수정한 하나 이상의 경기 자료
    """
    i = 0

    home_or_away_list = ["away_batter", "home_batter"]
    game_info = get_game_info(data["id"])
    for home_or_away in home_or_away_list:
        batters = data["contents"][home_or_away]
        # 타자 자료의 경우 필요 없는 키들이 있어서 리스트를 새로 만들어서 덮어씌우기
        fin_batters = []
        for batter in batters:
            new_info = {}
            new_info["idx"] = make_primary_key(
                batter["팀"],
                game_info["year"],
                game_info["month"],
                game_info["day"],
                game_info["더블헤더"],
            )
            new_info["name"] = change_long_name(batter["선수명"])
            new_info["team"] = batter["팀"]
            new_info["position"] = change_position(batter["포지션"])
            new_info = add_ining(Batter_factor, new_info, batter)
            new_info["hit"] = batter["안타"]
            new_info["bat_num"] = batter["타수"]
            new_info["hit_get"] = batter["타점"]
            new_info["own_get"] = batter["득점"]
            fin_batters.append(new_info)

        fin_batters = pd.DataFrame(fin_batters)
        data["contents"][home_or_away] = json.loads(
            fin_batters.to_json(orient="records")
        )
    i = i + 1

    return data


def change_position(data):
    """
    data = pandas DF
    사용방법
    import pandas as pd
    temp = pd.read_json("20210409_KTSS0.json")
    batter = pd.DataFrame(temp['20210409_KTSS0']["away_batter"])
    change_posision(batter)
    """
    pst = re.split("\B", data)

    for _ in pst:
        if "一" in data:
            data = data.replace("一", "3")
        elif "二" in data:
            data = data.replace("二", "4")
        elif "三" in data:
            data = data.replace("三", "5")
        elif "투" in data:
            data = data.replace("투", "1")
        elif "포" in data:
            data = data.replace("포", "2")
        elif "유" in data:
            data = data.replace("유", "6")
        elif "좌" in data:
            data = data.replace("좌", "7")
        elif "중" in data:
            data = data.replace("중", "8")
        elif "우" in data:
            data = data.replace("우", "9")
        elif "지" in data:
            data = data.replace("지", "D")
        elif "주" in data:
            data = data.replace("주", "R")
        elif "타" in data:
            data = data.replace("타", "H")
    return data


def add_ining(config, new_data, data):
    """
    이닝 수를 최대값인 18에 맞춰서 추가해주고 키 이름도 변경해주는 함수
    """

    for i in range(1, 19):
        if str(i) in data:
            # 키 이름 변경
            new_data["i_" + str(i)] = trans_code(config, str(data.pop(str(i))))
        else:
            # 데이터 추가
            new_data["i_" + str(i)] = "-"

    return new_data


def trans_code(config, data):
    """붙어있는 이닝 결과값들을 변환해주는 코드
    Args:
        data (sting): 한글로 기록된 타격기록
    Returns:
        data (int): "code_list.ini"로 변환된 코드
    """
    temp = [config[change_record(x)] for x in re.split("\W", data) if x != ""]

    return "".join(temp)


def change_record(data):
    """2010년 이전데이터에서 존재하는 타격기록의 한자를 숫자로 변경하는 함수
  
    ### Args:
        data (str): 한자가 포함된 타격기록

    ### Returns:
        temp_data (str): 숫자로 변경된 타격기록
    """
    data = data.replace("一","1")
    data = data.replace("二","2")
    data = data.replace("三","3")
    return data

def change_long_name(name):
    
    full_names = {"페르난데":"페르난데스","해즐베이":"해즐베이커","스몰린스":"스몰린스키","반슬라이":"반슬라이크"}
    if name in full_names.keys():
        return  full_names[name]
    else:
        return name
