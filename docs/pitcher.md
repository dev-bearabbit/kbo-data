# Pitcher

## Schema

DB에 저장하여 사용하실 분들은 아래의 DDL 쿼리를 사용하시면 됩니다.  
If you want to store data in DBMS, you can use the DDL query below.

```sql
CREATE TABLE pitcher(
    idx BIGINT(11) NOT NULL COMMENT "조합키(시합날짜+더블헤더+팀ID)",
    name VARCHAR(8) NOT NULL COMMENT "이름",
    team VARCHAR(4)  DEFAULT NULL COMMENT "팀이름",
    sp TINYINT(1) DEFAULT NULL COMMENT "선발",
    inning INT(3) DEFAULT NULL COMMENT "이닝",
    result VARCHAR(1) DEFAULT NULL COMMENT "결과",
    strikeout INT(2) DEFAULT NULL COMMENT "삼진",
    dead4ball INT(2) DEFAULT NULL COMMENT "4사구",
    losescore INT(2) DEFAULT NULL COMMENT "실점(R)",
    earnedrun INT(2) DEFAULT NULL COMMENT "자책",
    pitchnum INT(3) DEFAULT NULL COMMENT "투구수",
    hitted INT(3) DEFAULT NULL COMMENT "피안타(H)",
    homerun INT(2) DEFAULT NULL COMMENT "피홈런(HR)",
    battednum INT(2) DEFAULT NULL COMMENT "피타수",
    batternum INT(2) DEFAULT NULL COMMENT "피타자",
    CONSTRAINT scoreboards_pitcher_idx_fk FOREIGN KEY (idx) REFERENCES scoreboard (idx)
);
```

## Columns Info

|column name|term name|meaning|
|------------|-----------|---------|
|idx|조합키|"시합날짜+더블헤더+팀ID"로 구성된 외래 키. 경기정보 테이블인 scoreboard의 idx 컬럼을 참조한다.|
|name|이름|타자의 이름을 저장한다.|
|team|팀 이름|타자가 속한 팀 이름을 저장한다.|
|mound|선발|선발 여부를 저장한다. 기본값은 0이며, 선발인 경우는 1로 저장한다.|
|inning|이닝|얼마나 많은 타자를 아웃시켰는지를 나타낸다.(3단위) 마지막 인덱스의 숫자는 나머지이다.|
|result|경기결과|투수의 경기 결과를 저장한다. W:승, L:패, S:세이브, H:홀드|
|strikeout|삼진|삼진아웃을 시킨 수를 저장한다.|
|dead4ball|사사구|볼넷+데드볼을 발생시킨 수를 저장한다.|
|losescore|실점|투수의 책임이든 아니든 투수가 등판해 있을 때 상대에게 허용한 점수를 저장한다.|
|pitchnum|투구수|해당 게임에서 투구한 수를 저장한다.|
|hitted|피안타|타자가 안타를 친 수를 저장한다.|
|homerun|피홈런|타자가 홈런을 친 수를 저장한다.|
|battednum|피타수|타자가 친 공의 숫자를 저장한다.|
|batternum|피타자|상대한 타자 수를 저장한다.|
