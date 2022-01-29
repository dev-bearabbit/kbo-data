import datetime
import configparser
import os

# 설정파일을 읽어오기 위해 configparser를 사용
config = configparser.ConfigParser()
# 필요한 변수 가져오기
config.read(os.path.join(os.path.dirname(__file__),"config.ini"), encoding="utf-8")

def change_name_to_id(team_name, year):
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
        "KT": "KT"
    }

    if year >= 2021:
        return team_list_2021[team_name]
    else:
        return team_list[team_name]

def get_game_info(game_list):
    """입력된 정보를 토대로 해당 경기 연도, 날짜, 요일 등을 만드는 함수

    `20211115001`과 같은 정보가 들어오면 이를 가지고
    해당 경기 연도, 날짜, 요일 등을 만든다.

    Args:
        game_list (str): `20211115001`

    Returns:
        (dict): "year", "month", "day", "week", "더블헤더"를 키로 포함한다.
    """

    temp_date = game_list.split("_")[0]
    temp_date = datetime.datetime.strptime(temp_date.split("_")[0], "%Y%m%d")
    temp = {
        "year": temp_date.year,
        "month": temp_date.month,
        "day": temp_date.day,
        "week": temp_date.weekday(),
    }
    temp_team = game_list.split("_")[1]
    temp_team = {
        "더블헤더": int(temp_team[4:]),
    }
    temp.update(temp_team)

    return temp


def make_primary_key(team_name, year, month, day, dbheader):
    """스코어보드 DB에서 사용할 Primary Key를 작성하는 함수

    Examples:

        ```python
        year = 2021
        month = 4
        day = 29
        team_name = '두산'
        dbheader = 0

        import scoreboards
        scoreboards.make_primary_key(team_name, year, month, day, dbheader)
        '20210429001'
        ```

    Args:
        year (int):
        month (int) :
        day (int) :
        team_name (str) : 팀명 EG: 두산
        dbheader (int) : 더블해더 경기 유무.  아니다: 0, 1차전: 1, 2차전: 2

    Returns:
        (str): 숫자 길이가 11인 자연수. E.G.: '20210429001'
    """
    result = (
        str(year)
        + str(month).zfill(2)
        + str(day).zfill(2)
        + str(dbheader)
        + change_id_to_number(team_name).zfill(2)
    )
    return result


def change_id_to_number(team_name):
    """팀명을 팀 TeamID로 바꾸는 함수

    만약 빈 팀명이 들어오면, 히어로스 TeamID이 반환됩니다.
    2008~2009까지 스폰서가 없어서 "서울 히어로즈"라고 했지만,
    공식적으로 스폰서가 없었기 때문에 KBO에서는 "히어로즈"라고 명명하고 있다.
    그래서 빈 팀명이 들어오게 된다.

    Examples:

        ```python
        >>> import modifying
        >>> modifying.changing_team_name_into_id("두산")
        >>> '1'
        >>> modifying.changing_team_name_into_id("")
        >>> '8'
        ```

    Args:
        team_name (str): 팀명

    Returns:
        (str): 자연수 숫자
    """

    if team_name == "":
        return "8"
    else:
        return config["TEAM"][team_name]
