import ast
import pandas as pd

from kbodata.parser.util import make_primary_key, get_game_info

def scoreboard_modify(data):
    """수집한 여러개의 경기가 들어 있는 자료에서 스코어보드만 정리하는 함수
    이 함수는 여러 경기자료(`data`)에서 스코어보드만 뽑아서 내용을 고치고 변경한 다음
    다시 원 자료(`data`)에 끼워 넣는다. 즉 반환 값에는 모든 수집한 내용이 들어 있다.
    참고로 아래 긴 `for`문은 18회까지 연장하기 위한 방법이다. 기본적으로 현재 정규 이닝은
    13회까지밖에 없지만, 예전 정규 KBO 리그에서 18회까지 있는 경우가 있어 이를 반영했다.
    Note:
        현재 수정하고 있는 컬럼 이름
        - 이닝 이름 12개
        - 승패
        - 홈팀
        - 원정팀
        - 더블헤더
    Args:
        data (json): 수집한 하나 이상의 경기 자료
    Returns:
        data (json): scoreboard만 수정한, 하나 이상의 경기 자료
    """
    i = 0
    fin_boards = []
    etc_info = data["contents"]["ETC_info"]
    game_info = get_game_info(data["id"])
    home = data["contents"]["scoreboard"][1]["팀"]
    away = data["contents"]["scoreboard"][0]["팀"]
    for old_info in data["contents"]["scoreboard"]:
        new_info = {}
        new_info["idx"] = make_primary_key(
            old_info["팀"],
            game_info["year"],
            game_info["month"],
            game_info["day"],
            game_info["더블헤더"],
            )
        new_info["team"] = old_info["팀"]
        new_info["result"] = 1 if old_info["승패"] == "승" else 0 if old_info["승패"] == "무" else -1
        new_info = add_ining(new_info, old_info)
        new_info["r"] = old_info['R']
        new_info["h"] = old_info['H']
        new_info["e"] = old_info['E']
        new_info["b"] = old_info['B']
        new_info["year"] = game_info["year"]
        new_info["month"] = game_info["month"]
        new_info["day"] = game_info["day"]
        new_info["week"] = game_info["week"]
        new_info["home"]= home
        new_info["away"] = away
        new_info["dbheader"] = game_info["더블헤더"]
        new_info["place"] = etc_info["구장"]
        new_info["audience"] = int(etc_info["관중"].replace(',','')) if len(etc_info["관중"]) > 0 else 0
        new_info["starttime"] =  etc_info["개시"]
        new_info["endtime"] =  etc_info["종료"]
        new_info["gametime"] =  etc_info["경기시간"]
        fin_boards.append(new_info)

    fin_boards = pd.DataFrame(fin_boards)
    data["contents"]["scoreboard"] = ast.literal_eval(
            fin_boards.to_json(orient="records")
    )
    i = i + 1

    return data

def add_ining(new_data, data):
    """이닝 수를 최대값인 18에 맞춰서 추가해주고 키 이름도 변경해주는 함수
    """

    for i in range(1, 19):
        if str(i) in data:
            new_data["i_"+str(i)] = data[str(i)]
        else:
            # 데이터 추가
            new_data["i_" + str(i)] = "-"

    return new_data
