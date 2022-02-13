# What is kbo-data

kbo-data는 한국프로야구 경기정보를 스크래핑하는 파이썬 패키지입니다.  
kbo-data is a Python package that provides Korean professional baseball game information by scraping.

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kbodata)
[![PyPI](https://img.shields.io/pypi/v/kbodata)](https://pypi.org/project/kbodata/)
[![GitHub license](https://img.shields.io/github/license/Hyeonji-Ryu/kbo-data)](https://github.com/Hyeonji-Ryu/kbo-data/blob/main/LICENSE)

## Required

이 패키지를 사용하기 위해서는 chrome driver가 필요합니다. chrome driver는 [해당 페이지](https://chromedriver.chromium.org/downloads)에서 다운로드할 수 있습니다.  
This package is required chrome driver. You can download it from [this page](https://chromedriver.chromium.org/downloads)

## How to Use

### 패키지 설치하기

먼저 패키지를 설치합니다.  
you have to install kbodata package first.

```bash
pip install kbodata
```

### 데이터 가져오기 (kbodata.get module)

원하는 날짜의 경기 스케쥴을 다운로드 받습니다.  
you can download KBO match schedule that you want to get.

```python
    import kbodata

    # 2021년 4월 20일의 KBO 경기 스케쥴을 가져옵니다.
    # Get the KBO match schedule for April 20, 2021.
    >>> day = kbodata.get_daily_schedule(2021,4,20,'chromedriver_path')

    # 2021년 4월 KBO 경기 스케쥴을 가져옵니다.
    # Get the KBO match schedule for April 2021.
    >>> month = kbodata.get_monthly_schedule(2021,4,'chromedriver_path')

    # 2021년 KBO 경기 스케쥴을 가져옵니다. 
    # Get the KBO match schedule for 2021.
    >>> year = kbodata.get_yearly_schedule(2021,'chromedriver_path')
```

해당 스케쥴을 바탕으로 경기 정보를 JSON 형식으로 가져옵니다.  
It will be broght match information in JSON format based on the schedule.  

```python
    # 2021년 4월 20일의 KBO 경기 정보를 가져옵니다.
    # Get the KBO match information for April 20, 2021.
    >>> day_data = kbodata.get_game_data(day,'chromedriver_path')

    # 2021년 4월 KBO 경기 정보를 가져옵니다.
    # Get the KBO match information for April 2021.
    >>> month_data = kbodata.get_game_data(month,'chromedriver_path')

    # 2021년 KBO 경기 정보를 가져옵니다. 
    # Get the KBO match information for 2021.
    >>> year_data = kbodata.get_game_data(year,'chromedriver_path')
```

JSON 형식은 아래와 같습니다.  
The JSON format is as below.

```ini
    { id: date_gameid,
    contents: {
      'scoreboard': []
      'ETC_info': {}
      'away_batter': []
      'home_batter': []
      'away_pitcher': []
      'home_pitcher': []
        }
    }
```

## 데이터 변형하기 (kbodata.load module)

가져온 데이터들을 특정 파일 타입으로 변환합니다. 지원하는 파일 타입은 아래와 같습니다.  
This module converts data into specific file types. The supported file types are as follows.

- DataFrame(pandas)
- Dict

```python
    # 팀 경기 정보만을 정리하여 DataFrame으로 변환합니다.
    scoreboard = kbodata.scoreboard_to_DataFrame(day_data)
    # 타자 정보만을 정리하여 DataFrame으로 변환합니다.
    batter = kbodata.batter_to_DataFrame(day_data)
    # 투수 정보만을 정리하여 DataFrame으로 변환합니다.
    pitcher = kbodata.pitcher_to_DataFrame(day_data)

    # 팀 경기 정보만을 정리하여 Dict으로 변환합니다.
    scoreboard = kbodata.scoreboard_to_Dict(day_data)
    # 타자 정보만을 정리하여 Dict으로 변환합니다.
    batter = kbodata.batter_to_Dict(day_data)
    # 투수 정보만을 정리하여 Dict으로 변환합니다.
    pitcher = kbodata.pitcher_to_Dict(day_data)
```

변환된 데이터에 대한 정보는 아래의 링크에서 확인할 수 있습니다.  
You can find information about the converted data at the link below.

- Scoreboard: https://github.com/Hyeonji-Ryu/kbo-data/blob/main/docs/scoreboard.md
- Batter: https://github.com/Hyeonji-Ryu/kbo-data/blob/main/docs/batter.md
- Pitcher: https://github.com/Hyeonji-Ryu/kbo-data/blob/main/docs/pitcher.md

## Issues

KBO 공식 홈페이지에 없는 데이터는 제공되지 않습니다. 데이터가 제공되지 않는 경기 정보는 아래와 같습니다.  
Data that is not on the KBO official website is not provided. Match information for which data is not provided are listed below.  

### 경기 기준 (from game)

- 2008-03-30 LTHH0
- 2009-04-04 WOLT0
- 2010-03-20 OBLT0
- 2010-03-20 WOSS0
- 2015-07-08 HTWO0
- 2018-08-01 WOSK0

### 날짜 기준 (from date)

- 2013-03-09
- 2013-03-10
- 2013-03-11
- 2013-03-12
- 2013-03-13
- 2013-03-14
- 2013-03-15
- 2013-03-16
- 2013-03-17
- 2013-03-18
- 2013-03-19
- 2013-03-20
