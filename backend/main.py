import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import get_connection, init_db

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app = FastAPI(title="대출 상품 추천 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def no_cache(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store"
    return response


@app.on_event("startup")
def on_startup():
    init_db()


def row_to_product(row: dict) -> dict:
    return {
        "id": row["id"],
        "name": row["name"],
        "description": row["description"],
        "rate_display": row["rate_display"],
        "rate_min": row["rate_min"],
        "limit_display": row["limit_display"],
        "max_amount": row["max_amount"],
        "url": row["url"],
        "jobs": json.loads(row["jobs"]),
        "credits": json.loads(row["credits"]),
        "purposes": json.loads(row["purposes"]),
        "collaterals": json.loads(row["collaterals"]),
        "regions": json.loads(row["regions"]),
        "tags": json.loads(row["tags"]),
        "available": bool(row["available"]),
    }


@app.get("/api/products")
def list_products():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM loan_products ORDER BY rate_min ASC").fetchall()
    conn.close()
    return [row_to_product(dict(r)) for r in rows]


@app.get("/api/recommend")
def recommend(
    job: str = Query(..., description="직업 유형: 전체 / 직장인 / 자영업자 / 의료사업자 / 법인"),
    credit: str = Query(..., description="신용 등급: 전체 / 고신용 / 중신용 / 저신용"),
    purpose: str = Query(..., description="대출 목적: 전체 / 생활자금 / 사업자금 / 부동산 / 경매"),
    amount: int = Query(..., ge=1, description="필요 금액(만원)"),
    collateral: str = Query("없음", description="담보 여부: 없음 / 부동산 / 예적금"),
    region: str = Query("전국", description="거주/사업 지역: 전국 / 부산경남"),
):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM loan_products").fetchall()
    conn.close()

    products = [row_to_product(dict(r)) for r in rows]

    matched = []
    for p in products:
        if not p["available"]:
            continue
        if job != "전체" and job not in p["jobs"]:
            continue
        if credit != "전체" and credit not in p["credits"]:
            continue
        if purpose != "전체" and purpose not in p["purposes"]:
            continue
        if collateral not in p["collaterals"]:
            continue
        if region != "전국" and region not in p["regions"] and "전국" not in p["regions"]:
            continue
        if region == "전국" and "전국" not in p["regions"]:
            continue
        if amount > p["max_amount"]:
            continue
        matched.append(p)

    matched.sort(key=lambda p: (p["rate_min"], -p["max_amount"]))

    if matched:
        best_rate = matched[0]["rate_min"]
        for p in matched:
            p["best"] = p["rate_min"] == best_rate


    return {
        "query": {
            "job": job,
            "credit": credit,
            "purpose": purpose,
            "amount": amount,
            "collateral": collateral,
            "region": region,
        },
        "count": len(matched),
        "results": matched,
    }


app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
