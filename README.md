# IBK저축은행 대출 상품 추천 서비스

조건(직업/신용등급/목적/금액/담보/지역)을 입력하면 조건에 맞는 IBK저축은행 대출 상품을 추천하는 로컬 웹 서비스입니다.

## 구조

```
backend/    FastAPI 서버 (main.py, database.py, seed_data.py)
db/         SQLite 스키마(schema.sql)와 시드 데이터(products.json)
frontend/   정적 프론트엔드 (index.html)
start.sh    서버 기동 스크립트
stop.sh     서버 중지 스크립트
```

## 최초 설치 (PC당 한 번만)

사전 준비물: **Git**, **Python 3.12+** (설치 후 새 터미널을 열어야 PATH가 적용됩니다)

```
git clone https://github.com/sarchive-wave/recommand_loan.git
cd recommand_loan/backend
python -m pip install -r requirements.txt
python seed_data.py
```

`seed_data.py`는 `db/products.json`을 읽어 `db/loan.db`(SQLite, git에는 포함 안 됨)를 생성합니다. 상품 데이터를 수정했다면 다시 실행해서 재시드하면 됩니다.

## 실행 (매번)

Git Bash에서:

```
./start.sh   # http://127.0.0.1:8000 로 기동
./stop.sh    # 중지
```

`start.sh`는 PID를 `server.pid`에, 로그를 `server.log`에 남깁니다(둘 다 git 제외).

PowerShell에서 직접 실행하려면:

```
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

## API

- `GET /api/products` — 전체 상품 목록 (판매중단 포함, `available` 필드로 구분)
- `GET /api/recommend?job=&credit=&purpose=&amount=&collateral=&region=` — 조건에 맞는 상품 추천. `job`/`credit`/`purpose`는 `전체`를 넣으면 해당 조건을 걸지 않습니다.
