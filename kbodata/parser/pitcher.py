import json
import pandas as pd
from kbodata.parser.util import make_primary_key, get_game_info


def pitcher_modify(data):
    """수집한 여러 개의 경기가 들어 있는 자료에서 투수 자료만 정리하는 함수

    이 함수는 여러 경기자료(`data`)에서 스코어보드만 뽑아서 내용을 고치고 변경한 다음
    다시 원 자료(`data`)에 끼워 넣는다. 즉 반환 값에는 모든 수집한 내용이 들어 있다.
    참고로 아래 긴 `for`문은 18회까지 연장하기 위한 방법이다. 기본적으로 현재 정규 이닝은
    13회까지밖에 없지만, 예전 정규 KBO 리그에서 18회까지 있는 경우가 있어 이를 반영했다.

    Args:
        data (json): 수집한 하나 이상의 경기 자료

    Returns:
        data (json): 투수 자료만 수정한 하나 이상의 경기 자료
    """
    i = 0
    home_or_away_list = ["away_pitcher", "home_pitcher"]
    game_info = get_game_info(data["id"])
    for home_or_away in home_or_away_list:
        pitchers = data['contents'][home_or_away]
        # 투수 자료의 경우 필요 없는 키들이 있어서 리스트를 새로 만들어서 덮어씌우기
        fin_pitchers=[]
        for pitcher in pitchers:
            new_info={}
            new_info['idx'] = make_primary_key(pitcher["팀"], game_info["year"], game_info["month"], game_info["day"], game_info["더블헤더"])
            new_info['name'] = pitcher["선수명"]
            new_info['team'] = pitcher["팀"]
            new_info['mound'] = '1' if pitcher['등판'] == '선발' else '0'
            new_info['inning'] = change_inning(pitcher['이닝'])
            new_info['result'] = change_result(pitcher['결과'])
            new_info['strikeout'] = pitcher['삼진']
            new_info['dead4ball'] = pitcher['4사구']
            new_info['losescore'] = pitcher['실점']
            new_info['earnedrun'] = pitcher['자책']
            new_info['pitchnum'] = pitcher['투구수']
            new_info['hitted'] = pitcher['피안타']
            new_info['homerun'] = pitcher['홈런']
            new_info['battednum'] = pitcher['타수']
            new_info['batternum'] = pitcher['타자']
            fin_pitchers.append(new_info)

        fin_pitchers= pd.DataFrame(fin_pitchers)
        data["contents"][home_or_away] = json.loads(fin_pitchers.to_json(orient="records"))
    i = i + 1

    return data


def change_inning(data):
    """이닝수와 나머지를 정리해주는 코드. 이닝수와 나머지 값을 순차적으로 나열한다. 이닝수의 경우 0-18까지 가능하며, 나머지의 경우 0-2까지만 가능하다.

    ### Examples:
        - '5' -> 50
        - '2/3' -> 02
        - '1 2/3' -> 12
    """
    temp = str(data).split()
    
    if len(temp) == 1 and "/" not in temp[0]:
        return temp[0]+"0"
    elif len(temp) == 1 and "/" in temp[0]:
        return "0"+temp[-1][0]
    else:
        return temp[0] + temp[-1][0]

def change_result(result):

    if result == '세이브':
        return "S"
    elif result == "홀드":
        return "H"
    elif result == "승":
        return "W"
    else:
        return "L"
