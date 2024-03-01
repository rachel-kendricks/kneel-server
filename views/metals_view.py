import sqlite3
import json


def update_metal(id, metal_data):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        UPDATE Metals
            SET price = ?
        WHERE id = ?
            """,
            (metal_data["price"], id),
        )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False
