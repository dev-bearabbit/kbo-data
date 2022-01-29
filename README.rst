===================
What is kbo-data
===================

| kbo-data는 한국프로야구 경기정보를 스크래핑하는 파이썬 패키지입니다.
| kbo-data is a Python package that provides Korean professional baseball game information by scraping.

---------------
Required
---------------

| 이 패키지를 사용하기 위해서는 chrome driver가 필요합니다. chrome driver는 `해당 페이지 <https://chromedriver.chromium.org/downloads>`_ 에서 다운로드할 수 있습니다.  
| This package is required chrome driver. You can download it from `this page <https://chromedriver.chromium.org/downloads>`_

---------------
How to Use
---------------

데이터 가져오기 (kbodata.get module)
=======================================

| 1. 원하는 날짜의 경기 스케쥴을 다운로드 받습니다.  
| 1. you can download KBO match schedule that you want to get.

.. code-block:: python

    import kbodata

    # 2021년 4월 20일의 KBO 경기 스케쥴을 가져옵니다.
    # Get the KBO match schedule for April 20, 2021.
    >>> day = kbodata.get_daily_schedule(2021,4,20,'chromedriver')

    # 2021년 4월 KBO 경기 스케쥴을 가져옵니다.
    # Get the KBO match schedule for April 2021.
    >>> month = kbodata.get_monthly_schedule(2021,4,'chromedriver')

    # 2021년 KBO 경기 스케쥴을 가져옵니다. 
    # Get the KBO match schedule for 2021.
    >>> year = kbodata.get_yearly_schedule(2021,'chromedriver')


| 2. 해당 스케쥴을 바탕으로 경기 정보를 json 형식으로 가져옵니다.  
| 2. It will be broght match information in json format based on the schedule.  

.. code-block:: python

    # 2021년 4월 20일의 KBO 경기 정보를 가져옵니다.
    # Get the KBO match information for April 20, 2021.
    data1 = kbodata.get_game_data(day,'chromedriver')

    # 2021년 4월 KBO 경기 정보를 가져옵니다.
    # Get the KBO match information for April 2021.
    data2 = kbodata.get_game_data(month,'chromedriver')

    # 2021년 KBO 경기 정보를 가져옵니다. 
    # Get the KBO match information for 2021.
    data3 = kbodata.get_game_data(year,'chromedriver')

Json 형식은 아래와 같습니다.

.. code-block:: python
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

데이터 변형하기 (kbodata.load module)
=======================================

| 가져온 데이터들을 원하는 파일 타입으로 변환합니다. 지원하는 파일 타입은 아래와 같습니다.


---------------
Issues
---------------

| KBO 공식 홈페이지에 없는 데이터는 제공되지 않습니다. 데이터가 제공되지 않는 경기 정보는 아래와 같습니다.  
| Data that is not on the KBO official website is not provided. Match information for which data is not provided are listed below.  
| 
- 2008-03-30 LTHH0
- 2009-04-04 WOLT0
- 2015-07-08 HTWO0
- 2018-08-01 WOSK0
