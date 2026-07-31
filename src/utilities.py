import sqlite3


def init_db_connection() -> sqlite3.Cursor:
    connection = sqlite3.connect("ecommerce.db")
    return connection.cursor()


def destroy_db_connection(cursor: sqlite3.Cursor) -> None:
    cursor.close()


def _create_tables(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""
    CREATE TABLE Customer (
        CustomerID INTEGER PRIMARY KEY,
        Name TEXT,
        Email TEXT
    );

    CREATE TABLE Product (
        ProductID INTEGER PRIMARY KEY,
        Name TEXT,
        Price DECIMAL(8,2),
        Stock INTEGER
    );
    """)
