# Scoreboard

## Columns Info

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
    week INT(1) DEFAULT NULL COMMENT "주",
    home VARCHAR(4) DEFAULT NULL COMMENT "홈팀",
    away VARCHAR(4) DEFAULT NULL COMMENT "원정팀",
    dbheader INT(1) DEFAULT NULL COMMENT "더블헤더",
    judge VARCHAR(35) DEFAULT NULL COMMENT "심판",
    place VARCHAR(3) DEFAULT NULL COMMENT "구장",
    audience INT(6) DEFAULT NULL COMMENT "관중",
    starttime CHAR(5) DEFAULT NULL  COMMENT "개시",
    endtime CHAR(5) DEFAULT NULL  COMMENT "종료",
    gametime CHAR(5) DEFAULT NULL  COMMENT "경기시간",
    PRIMARY KEY (`idx`)
);
```
