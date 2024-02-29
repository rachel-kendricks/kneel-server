import sqlite3
import json


def get_all_orders(url):
    if url["query_params"]:
        return "all orders getted with expand! ;)"
    else:
        with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
            SELECT
                o.*
            FROM Orders o
            """
            )
            query_results = db_cursor.fetchall()

            orders = []
            for row in query_results:
                orders.append(dict(row))

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
