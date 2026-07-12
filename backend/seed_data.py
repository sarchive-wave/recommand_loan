import json
from pathlib import Path

from database import get_connection, init_db

PRODUCTS_PATH = Path(__file__).resolve().parent.parent / "db" / "products.json"


def seed():
    conn = get_connection()
    conn.execute("DROP TABLE IF EXISTS loan_products")
    conn.commit()
    conn.close()
    init_db()

    conn = get_connection()
    cur = conn.cursor()

    with open(PRODUCTS_PATH, "r", encoding="utf-8") as f:
        products = json.load(f)

    for p in products:
        cur.execute(
            """
            INSERT INTO loan_products
                (name, description, rate_display, rate_min, limit_display, max_amount,
                 url, jobs, credits, purposes, collaterals, regions, tags, available)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                p["name"],
                p["description"],
                p["rate_display"],
                p["rate_min"],
                p["limit_display"],
                p["max_amount"],
                p["url"],
                json.dumps(p["jobs"], ensure_ascii=False),
                json.dumps(p["credits"], ensure_ascii=False),
                json.dumps(p["purposes"], ensure_ascii=False),
                json.dumps(p["collaterals"], ensure_ascii=False),
                json.dumps(p["regions"], ensure_ascii=False),
                json.dumps(p["tags"], ensure_ascii=False),
                1 if p.get("available", True) else 0,
            ),
        )

    conn.commit()
    count = cur.execute("SELECT COUNT(*) FROM loan_products").fetchone()[0]
    conn.close()
    print(f"Seeded {count} loan products into {Path('db/loan.db')}")


if __name__ == "__main__":
    seed()
