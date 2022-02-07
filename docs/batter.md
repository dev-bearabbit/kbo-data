# Batter

## Columns Info

## Schema

DB에 저장하여 사용하실 분들은 아래의 DDL 쿼리를 사용하시면 됩니다.  
If you want to store data in DBMS, you can use the DDL query below.

```sql
CREATE TABLE batter(
    idx BIGINT(11) NOT NULL COMMENT "조합키(시합날짜+더블헤더+팀ID)",
    playerid INT(5) NOT NULL COMMENT "선수ID",
    team VARCHAR(4)  DEFAULT NULL COMMENT "팀이름",
    position VARCHAR(2) DEFAULT NULL COMMENT "포지션",
    i_1 INT(8) DEFAULT NULL COMMENT "1이닝",
    i_2  INT(8) DEFAULT NULL COMMENT "2이닝",
    i_3  INT(8) DEFAULT NULL COMMENT "3이닝",
    i_4  INT(8) DEFAULT NULL COMMENT "4이닝",
    i_5  INT(8) DEFAULT NULL COMMENT "5이닝",
    i_6  INT(8) DEFAULT NULL COMMENT "6이닝",
    i_7  INT(8) DEFAULT NULL COMMENT "7이닝",
    i_8  INT(8) DEFAULT NULL COMMENT "8이닝",
    i_9  INT(8) DEFAULT NULL COMMENT "9이닝",
    i_10  INT(8) DEFAULT NULL COMMENT "10이닝",
    i_11  INT(8) DEFAULT NULL COMMENT "11이닝",
    i_12  INT(8) DEFAULT NULL COMMENT "12이닝",
    i_13  INT(8) DEFAULT NULL COMMENT "13이닝",
    i_14  INT(8) DEFAULT NULL COMMENT "14이닝",
    i_15  INT(8) DEFAULT NULL COMMENT "15이닝",
    i_16  INT(8) DEFAULT NULL COMMENT "16이닝",
    i_17  INT(8) DEFAULT NULL COMMENT "17이닝",
    i_18  INT(8) DEFAULT NULL COMMENT "18이닝",
    hit  INT(2) DEFAULT NULL COMMENT "안타수(H)",
    bat_num  INT(2) DEFAULT NULL COMMENT "타수(AB)",
    hit_get  INT(2) DEFAULT NULL COMMENT "타점(RBI)",
    own_get  INT(2) DEFAULT NULL COMMENT "득점(R)",
    CONSTRAINT scoreboards_batter_idx_fk FOREIGN KEY (idx) REFERENCES scoreboard (idx),
    CONSTRAINT player_id_batter_playerid_fk FOREIGN KEY (playerid) REFERENCES player_id (playerid)
);
```
