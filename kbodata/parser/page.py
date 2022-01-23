import ast
import os
import configparser
from selenium import webdriver
from bs4 import BeautifulSoup

from kbodata.parser.html import scoreboard, etc_info, looking_for_team_names
from kbodata.parser.html import away_batter, home_batter, away_pitcher, home_pitcher

# 설정파일을 읽어오기 위해 configparser를 사용
config = configparser.ConfigParser()
# 필요한 변수 가져오기
config.read(os.path.join(os.path.dirname(__file__),"config.ini"), encoding="utf-8")
print(os.path.join(os.path.dirname(__file__),"config.ini"))
url = config["DEFAULT"]["KBO_URL"]


def get_page(gameDate, gameId, Driver_path):
    """
    단일 게임 페이지의 내용을 chromium을 이용해 가져오는 함수

    속도를 조금이나마 빠르게 하기 위해서 lxml을 사용하고 있다.
    이렇게 받은 자료는 그냥 받기만 한 수준이기 때문에
    내부에 HTML 코드가 들어 있어 데이터 분석에 사용할 수 없다.

    참고
    ---
    driver.implicitly_wait(3) : 이 정도 기다려야 페이지를 잘 받을 수 있다.

    Example
    -------
        >>> temp_page=get_page("20181010","KTLT1")

    Parameters
    ----------
    param1: str
        gameDate: "20181010" 와 같이 경기 날짜로 만들어진 문자열

    param1: str
        gameld: 경기를 하는 팀명과 더블해더 유무를 이용해 만든 문자열
        "WOOB0"과 같이 만드는데, WO, OB는 각각 팀명을 의미하고
        0은 더블헤더 경기가 아닌 것을 알려준다.
        만약 더불헤더 경기면 1차전은 "KTLT1"처럼 1로 표시하고
        2차전이면 "KTLT2"으로 표시한다.

    Returns
    -------
        json
            다음과 같은 항목으로 수입하고 있는 페이지에서 가져온 자료를 그대로 저장한다.

            - 'tables': 게임 자료
            - 'record_etc' : 구장, 관중, 개시 시간, 종료 시간, 경기시간
            - 'teams' e.g.:('KT', '롯데')
            - 'date': e.g.: '20181010'
            - 'id': e.g.: 'KTLT1'
    """
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("window-size=1920x1080")
        options.add_argument("disable-gpu")
        # 혹은 options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(Driver_path, chrome_options=options)
        # 주소 보기
        # 20180801&amp;gameId=20180801WOSK0&amp;section=REVIEW
        temp_url = url + gameDate + "&amp;gameId=" + gameDate + gameId + "&amp;section=REVIEW"
        driver.get(temp_url)
        driver.implicitly_wait(5)
        soup = BeautifulSoup(driver.page_source, "lxml")
        tables = soup.find_all("table")
        record_etc = soup.findAll("div", {"class": "record-etc"})
        box_score = soup.findAll("div", {"class": "box-score-wrap"})

        # 2021년 5월 12일 현재, h6는 팀 명에서만 사용한다.
        temp_teams = soup.findAll("h6")
        teams = looking_for_team_names(temp_teams)

        return {
            "tables": tables,
            "record_etc": record_etc,
            "teams": teams,
            "date": gameDate,
            "id": gameId,
        }

    except Exception as e:
        print()

    finally:
        driver.quit()


def parsing_single_game(date, gameId, Driver_path):
    """
    다운받은 단일 게임 자료를 사용하기 쉽게 원본을 보존하며 적절하게 정리하는 함수

    `getting_page()`을 통해 받은 단일 게임 자료를
    데이터 분석하기 위해 modify 하기 쉽도록 다운받은 내용 그대로 유지하면서
    내용을 추가하지 않고 필요하지 않은 부분, 예를 들어 HTML 관련 코드 등을 정리한다.
    이렇게 처리하는 이유는 다운받은 것을 거의 원본 그대로 보관하면
    이 자료를 다룰 때 문제점이 발생하더라도 다운을 다시 받을 필요가 없기 때문이다.

    Example
    -------
        >>> temp_page = single_game("20181010","KTLT1")

    Parameters
    ----------
    :param1: str
        date: "20181010" 와 같이 경기 날짜로 만들어진 문자열
    :param1: str
        gameld: 경기를 하는 팀명과 더블해더 유무를 이용해 만든 문자열
        "WOOB0"과 같이 만드는데, WO, OB는 각각 팀명을 의미하고
        0은 더블헤더 경기가 아닌 것을 알려준다.
        만약 더불헤더 경기면 1차전은 "KTLT1"처럼 1로 표시하고
        2차전이면 "KTLT2"으로 표시한다.

    Returns
    -------
        json
        게임 자료가 들어 있다. "id" 키에는 '20181010_KTLT1' 과 같은
        정규 시즌 단일 게임 아이디가 들어 있다. Parameters를 이용해서 만든다.
        "contents" 키에는 다음 키가 들어 있고 각 키에는 해당 게임 정보가 들어 있다.

        - 'scoreboard'
        - 'ETC_info'
        - 'away_batter'
        - 'home_batter'
        - 'away_pitcher'
        - 'home_pitcher'
    """

    temp_page = get_page(date, gameId, Driver_path)
    temp_scoreboard = scoreboard(temp_page["tables"], temp_page["teams"])

    temp_all = {
        "scoreboard": ast.literal_eval(temp_scoreboard.to_json(orient="records"))
    }
    temp_all.update(
        {"ETC_info": etc_info(temp_page["tables"], temp_page["record_etc"])}
    )
    temp_all.update(
        {
            "away_batter": ast.literal_eval(
                away_batter(temp_page["tables"], temp_page["teams"]).to_json(
                    orient="records"
                )
            )
        }
    )
    temp_all.update(
        {
            "home_batter": ast.literal_eval(
                home_batter(temp_page["tables"], temp_page["teams"]).to_json(
                    orient="records"
                )
            )
        }
    )
    temp_all.update(
        {
            "away_pitcher": ast.literal_eval(
                away_pitcher(temp_page["tables"], temp_page["teams"]).to_json(
                    orient="records"
                )
            )
        }
    )
    temp_all.update(
        {
            "home_pitcher": ast.literal_eval(
                home_pitcher(temp_page["tables"], temp_page["teams"]).to_json(
                    orient="records"
                )
            )
        }
    )

    temp_name = temp_page["date"] + "_" + temp_page["id"]
    return {"id": temp_name, "contents": temp_all}
