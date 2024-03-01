import sqlite3
import json


def get_all_orders(url):

    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                o.size_id,
                o.style_id,
                o.metal_id,
                m.id,
                m.metal,
                m.price metal_price,
                st.id,
                st.style,
                st.price style_price,
                si.id,
                si.carete,
                si.price size_price

            FROM `Orders` o
            JOIN Metals m ON m.id = o.metal_id
            JOIN Styles st ON o.style_id = st.id
            JOIN Sizes si ON o.size_id = si.id
            """
        )
        query_results = db_cursor.fetchall()

        orders = []
        for row in query_results:

            metal = {
                "metal_name": row["metal"],
                "metal_price": row["metal_price"],
            }
            style = {
                "style_name": row["style"],
                "style_price": row["style_price"],
            }
            size = {
                "size_name": row["carete"],
                "size_price": row["size_price"],
            }
            order = {
                "metal_id": row["metal_id"],
                "style_id": row["style_id"],
                "size_id": row["size_id"],
                "metal": metal,
                "style": style,
                "size": size,
            }

            orders.append(order)

        serialized_ships = json.dumps(orders)

    return serialized_ships


def get_single_order(pk, url):
    if url["query_params"]:
        return "single order gotten with expand!"

    else:
        with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
            SELECT o.*
            FROM Orders o
            WHERE o.id = ?
                """,
                (pk,),
            )
            query_results = db_cursor.fetchone()

            dictionary_version_of_object = dict(query_results)
            serialized_ship = json.dumps(dictionary_version_of_object)

        return serialized_ship


def create_order(order_info):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO orders(metal_id, style_id, size_id)
        VALUES(?,?,?)
            """,
            (order_info["metal_id"], order_info["style_id"], order_info["size_id"]),
        )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False


def delete_order(pk):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        DELETE FROM Orders WHERE id = ?
            """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False
