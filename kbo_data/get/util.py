def change_name_into_id(team_name, year):
    """팀 이름을 팀 ID로 바꾸는 함수

    2021년 SSG가 창단했다. 그래서 팀명이 SK에서 SSG로 변경되었다.
    그러나 KBO 홈피에서 사용하는 ID는 안 바꾼 것 같다.
    그래서 팀명을 KBO에서 바꾸는 함수를 새로 만들었다.

    Args:
        team_name (str): 팀명

    """

    team_list_2021 = {
        "KIA": "HT",
        "두산": "OB",
        "롯데": "LT",
        "NC": "NC",
        "SSG": "SK",
        "LG": "LG",
        "넥센": "WO",
        "키움": "WO",
        "히어로즈": "WO",
        "우리": "WO",
        "한화": "HH",
        "삼성": "SS",
        "KT": "KT",
    }
    team_list = {
        "KIA": "HT",
        "두산": "OB",
        "롯데": "LT",
        "NC": "NC",
        "SK": "SK",
        "LG": "LG",
        "넥센": "WO",
        "키움": "WO",
        "히어로즈": "WO",
        "우리": "WO",
        "한화": "HH",
        "삼성": "SS",
        "KT": "KT",
    }

    if year >= "2021":
        return team_list_2021[team_name]
    else:
        return team_list[team_name]
