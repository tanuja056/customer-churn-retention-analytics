
import sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "processed" / "customer_churn_clean.csv"
DB_FILE = ROOT / "data" / "processed" / "customer_churn.db"
SQL_FILE = ROOT / "sql" / "churn_analysis.sql"

# Load cleaned data into SQLite
df = pd.read_csv(DATA_FILE)

with sqlite3.connect(DB_FILE) as conn:
    df.to_sql("customers", conn, if_exists="replace", index=False)

    print("\nDATABASE CREATED")
    print(f"Customers loaded: {len(df):,}")

    # Execute SQL analysis
    sql = SQL_FILE.read_text(encoding="utf-8")
    for i, statement in enumerate(sql.split(";"), start=1):
        if statement.strip():
            print(f"\n{'=' * 60}")
            print(f"SQL ANALYSIS {i}")
            print("=" * 60)
            result = pd.read_sql_query(statement, conn)
            print(result.to_string(index=False))

print("\nSQL analysis completed.")
