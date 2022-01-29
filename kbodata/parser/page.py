import ast
import os
import configparser
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from kbodata.parser.html import scoreboard, etc_info, looking_for_team_names
from kbodata.parser.html import away_batter, home_batter, away_pitcher, home_pitcher

# 설정파일을 읽어오기 위해 configparser를 사용
config = configparser.ConfigParser()
# 필요한 변수 가져오기
config.read(os.path.join(os.path.dirname(__file__),"config.ini"), encoding="utf-8")
url = config["DEFAULT"]["KBO_URL"]


def parsing_page(gameDate, gameId, driver):
    temp_url = url + gameDate + "&amp;gameId=" + gameDate + gameId + "&amp;section=REVIEW"
    driver.get(temp_url)
    data = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.ID,"gameCenterContents")))
    soup = BeautifulSoup(data.get_attribute('innerHTML'), "lxml")
    tables = soup.find_all("table")
    record_etc = soup.findAll("div", {"class": "record-etc"})
    temp_teams = soup.findAll("h6")
    teams = looking_for_team_names(temp_teams)

    return {
        "tables": tables,
        "record_etc": record_etc,
        "teams": teams,
        "date": gameDate,
        "id": gameId,
    }


def parsing_single_game(date, gameId, driver):
    """
    다운받은 단일 게임 자료를 사용하기 쉽게 원본을 보존하며 적절하게 정리하는 함수

    `get_page()`을 통해 받은 단일 게임 자료를
    데이터 분석하기 위해 modify 하기 쉽도록 다운받은 내용 그대로 유지하면서
    내용을 추가하지 않고 필요하지 않은 부분, 예를 들어 HTML 관련 코드 등을 정리한다.
    이렇게 처리하는 이유는 다운받은 것을 거의 원본 그대로 보관하면
    이 자료를 다룰 때 문제점이 발생하더라도 다운을 다시 받을 필요가 없기 때문이다.

    Example
    -------
    >>> temp_page = parsing_single_game("20181010","KTLT1", driver)

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

    temp_page = parsing_page(date, gameId, driver)

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
