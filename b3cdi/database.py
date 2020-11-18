from datetime import datetime
import math
import pandas as pd
import sqlite3
from typing import Tuple


def get_db_connection(output_dir) -> sqlite3.Connection:

    filepath = output_dir + "cdi.db"
    conn = sqlite3.connect(filepath)
    db_cursor = conn.cursor()
    db_cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='cdi';"
    )

    if not db_cursor.fetchone():
        conn.execute(
            "CREATE TABLE cdi"
            "(date TEXT, base252 REAL, base360 REAL, duration INTEGER);"
        )

    db_cursor.close()
    return conn


def get_latest_date(db_conn: sqlite3.Connection) -> Tuple[bool, pd.Timestamp]:

    db_cursor = db_conn.cursor()
    db_cursor.execute("SELECT date FROM cdi ORDER BY date DESC LIMIT 1;")

    result = db_cursor.fetchone()
    db_cursor.close()

    if result is None or len(result) == 0:
        return (False, None)

    formated_date = datetime.strptime(result[0], "%Y-%m-%d")

    return (True, pd.Timestamp(formated_date, tz=None))


def insert_data(dt: pd.Timestamp, df: pd.DataFrame, db_conn: sqlite3.Connection):
    db_cursor = db_conn.cursor()

    bases = ["base252", "base360"]
    date = dt.strftime("%Y-%m-%d")

    for row in df.itertuples():
        doc = {
            "date": f"'{date}'",
            "duration": str(getattr(row, "duration")),
        }

        for base in bases:
            val = getattr(row, base)
            if math.isnan(val):
                continue
            doc[base] = str(val)

        if any([d in doc for d in bases]):
            columns = ", ".join(doc.keys())
            values = ", ".join(doc.values())
            query = f"INSERT INTO cdi ({columns}) VALUES ({values});"
            db_cursor.execute(query)

    db_conn.commit()
    db_cursor.close()
