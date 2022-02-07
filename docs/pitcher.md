# Pitcher

## Columns Info

## Schema

DB에 저장하여 사용하실 분들은 아래의 DDL 쿼리를 사용하시면 됩니다.  
If you want to store data in DBMS, you can use the DDL query below.

```sql
CREATE TABLE pitcher(
    idx BIGINT(11) NOT NULL COMMENT "조합키(시합날짜+더블헤더+팀ID)",
    playerid INT(5) NOT NULL COMMENT "선수ID",
    team VARCHAR(4)  DEFAULT NULL COMMENT "팀이름",
    mound TINYINT(1) DEFAULT NULL COMMENT "선발",
    inning INT(1) DEFAULT NULL COMMENT "이닝",
    result VARCHAR(3) DEFAULT NULL COMMENT "결과",
    strikeout INT(2) DEFAULT NULL COMMENT "삼진",
    dead4ball INT(2) DEFAULT NULL COMMENT "4사구",
    losescore INT(2) DEFAULT NULL COMMENT "실점",
    earnedrun INT(2) DEFAULT NULL COMMENT "자책",
    pitchnum INT(3) DEFAULT NULL COMMENT "투구수",
    hitted INT(2) DEFAULT NULL COMMENT "피안타",
    homerun INT(2) DEFAULT NULL COMMENT "피홈런",
    battednum INT(2) DEFAULT NULL COMMENT "피타수",
    batternum INT(2) DEFAULT NULL COMMENT "피타자",
    CONSTRAINT scoreboards_pitcher_idx_fk FOREIGN KEY (idx) REFERENCES scoreboard (idx),
    CONSTRAINT player_id_pitcher_playerid_fk FOREIGN KEY (playerid) REFERENCES player_id (playerid)
);
```
