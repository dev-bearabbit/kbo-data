# What is kbo-data

kbo-data는 한국프로야구 경기정보를 스크래핑하는 파이썬 패키지입니다.  
kbo-data is a Python package that provides Korean professional baseball game information by scraping.

## Required

이 패키지를 사용하기 위해서는 chrome driver가 필요합니다.  
chrome driver는 [해당 페이지](https://chromedriver.chromium.org/downloads)에서 다운로드할 수 있습니다.  
This package is required chrome driver.
You can download it from [this page](https://chromedriver.chromium.org/downloads)

## How to Use

### 데이터 가져오기 (kbodata.get module)

1. 원하는 날짜의 경기 스케쥴을 다운로드 받습니다.

    ```python
    import kbodata

    # 2021년 4월 20일의 KBO 경기 스케쥴을 가져옵니다.
    >>> test1 = kbodata.get_daily_schedule("20210420",'chromedriver')

    # 2021년 4월부터 2021년 5월까지의 KBO 경기 스케쥴을 가져옵니다.
    >>> test2 = kbodata.get_monthly_schedule("202104","202105",'chromedriver')
    # 2020년, 2021년 4월의 KBO 경기 스케쥴을 가져옵니다. 
    >>> test3 = kbodata.get_monthly_schedule("202004","202104",'chromedriver',True)
    ```

2. 해당 스케쥴을 바탕으로 경기 정보를 가져옵니다.

```python
    # KBO 경기정보를 dict 형식으로 가져옵니다.
    data1 = kbodata.get_game_data(test1,'chromedriver')
    data2 = kbodata.get_game_data(test2,'chromedriver')
    data3 = kbodata.get_game_data(test3,'chromedriver')
```

### 데이터 변형하기 (kbodata.load module)
