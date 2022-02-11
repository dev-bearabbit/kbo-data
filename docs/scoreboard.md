# Scoreboard

## Schema

DB에 저장하여 사용하실 분들은 아래의 DDL 쿼리를 사용하시면 됩니다.  
If you want to store data in DBMS, you can use the DDL query below.

```sql
CREATE TABLE scoreboard(
    idx BIGINT(11) NOT NULL COMMENT "조합키(시합날짜+더블헤더+팀ID)",
    team VARCHAR(4)  DEFAULT NULL COMMENT "팀이름",
    result INT(1) DEFAULT NULL COMMENT "결과",
    i_1 INT(2) DEFAULT NULL COMMENT  "1이닝",
    i_2 INT(2) DEFAULT NULL COMMENT  "2이닝",
    i_3 INT(2) DEFAULT NULL COMMENT  "3이닝",
    i_4 INT(2) DEFAULT NULL COMMENT  "4이닝",
    i_5 INT(2) DEFAULT NULL COMMENT  "5이닝",
    i_6 INT(2) DEFAULT NULL COMMENT  "6이닝",
    i_7 INT(2) DEFAULT NULL COMMENT  "7이닝",
    i_8 INT(2) DEFAULT NULL COMMENT  "8이닝",
    i_9 INT(2) DEFAULT NULL COMMENT  "9이닝",
    i_10 INT(2) DEFAULT NULL COMMENT  "10이닝",
    i_11 INT(2) DEFAULT NULL COMMENT  "11이닝",
    i_12 INT(2) DEFAULT NULL COMMENT  "12이닝",
    i_13 INT(2) DEFAULT NULL COMMENT  "13이닝",
    i_14 INT(2) DEFAULT NULL COMMENT  "14이닝",
    i_15 INT(2) DEFAULT NULL COMMENT  "15이닝",
    i_16 INT(2) DEFAULT NULL COMMENT  "16이닝",
    i_17 INT(2) DEFAULT NULL COMMENT  "17이닝",
    i_18 INT(2) DEFAULT NULL COMMENT  "18이닝",
    r INT(2) DEFAULT NULL COMMENT "득점",
    h INT(2) DEFAULT NULL COMMENT "안타",
    e INT(2) DEFAULT NULL COMMENT "실책",
    b INT(2) DEFAULT NULL COMMENT "사사구",
    year INT(4) DEFAULT NULL COMMENT "년도",
    month INT(2) DEFAULT NULL COMMENT "월",
    day INT(2) DEFAULT NULL COMMENT "일",
    week INT(1) DEFAULT NULL COMMENT "요일",
    home VARCHAR(4) DEFAULT NULL COMMENT "홈팀",
    away VARCHAR(4) DEFAULT NULL COMMENT "원정팀",
    dbheader INT(1) DEFAULT NULL COMMENT "더블헤더",
    place VARCHAR(3) DEFAULT NULL COMMENT "구장",
    audience INT(6) DEFAULT NULL COMMENT "관중",
    starttime CHAR(5) DEFAULT NULL  COMMENT "개시",
    endtime CHAR(5) DEFAULT NULL  COMMENT "종료",
    gametime CHAR(5) DEFAULT NULL  COMMENT "경기시간",
    PRIMARY KEY (`idx`)
);
```

## Columns Info

|column name|term name|meaning|
|------------|-----------|---------|
|idx|조합키|"시합날짜+더블헤더+팀ID"로 구성된 기본 키. 선수들 정보와 경기 정보를 연결한다.|
|team|팀 이름|팀 이름을 저장한다.|
|result|경기결과|승리는 int 1, 패배는 int -1, 무승부는 int 0 로 저장한다.|
|i_{1-18}|이닝점수|각 이닝마다의 점수를 저장한다. 점수가 없는 경우는 "-"가 저장된다.|
|r|득점|경기에서 얻은 총 득점의 수를 나타낸다.|
|h|안타|경기에서 얻은 총 안타의 수를 나타낸다.|
|e|실책|경기에서 얻은 총 실책의 수를 나타낸다.|
|b|사사구|경기에서 발생한 총 사사구(볼넷과 데드볼의 합)의 수를 나타낸다.|
|year|년도|경기 날짜의 년도만을 저장한다.|
|month|월|경기 날짜의 월만을 저장한다.|
|day|일|경기 날짜의 일만을 저장한다.|
|week|요일|경기가 진행한 날의 요일을 나타낸다. 0:월요일, 1:화요일, 2:수요일, 3:목요일, 4:금요일, 5:토요일, 6:일요일|
|home|홈팀|경기의 홈팀을 저장한다.|
|away|원정팀|경기의 원정팀을 저장한다.|
|dbheader|더블헤더|더불헤더가 아닌 날짜의 경기는 0, 더블헤더 첫 번째 경기는 1, 두 번째 경기는 2로 저장한다.|
|place|구장|경기가 일어난 구장 위치를 저장한다.|
|audience|관객 수|경기 관람에 참여한 관객 수를 저장한다.|
|starttime|개시시간|경기가 시작한 시간을 저장한다.|
|endtime|종료시간|경기가 끝난 시간을 저장한다.|
|gametime|경기시간|경기에 소요된 시간을 저장한다.|

### Team ID

컬럼 `idx`에 사용되는 팀 ID는 아래와 같다.

```ini
두산: 1
롯데: 2
삼성: 3
한화: 4
LG: 5
KIA: 6
SK: 7
현대: 8
우리: 8
넥센: 8
키움: 8
서울: 8
NC: 9
KT: 10
SSG: 11
```
