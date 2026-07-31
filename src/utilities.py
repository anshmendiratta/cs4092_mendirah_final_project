import sqlite3
from typing import List


def init_db_connection() -> [sqlite3.Connection, sqlite3.Cursor]:
    connection = sqlite3.connect("ecommerce.db")
    return (connection, connection.cursor())


def destroy_db_connection(cursor: sqlite3.Cursor) -> None:
    cursor.close()


# NOTE: needed to overwrite previous saves to the table.
def destroy_tables(cursor: sqlite3.Cursor) -> None:
    tables: List = cursor.fetchall()

    for table in tables:
        name = table[0]
        cursor.execute(f'DROP TABLE IF EXISTS "{name}";')


def create_tables(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""
        CREATE TABLE Customer (
            CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,

            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE,
            Phone TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE Staff (
            StaffID INTEGER PRIMARY KEY AUTOINCREMENT,

            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Position TEXT NOT NULL
        );
     """)

    cursor.execute("""
        CREATE TABLE Product (
            ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
            StaffID INTEGER NOT NULL,

            Name TEXT NOT NULL,
            Description TEXT,
            Price REAL NOT NULL
                CHECK (Price >= 0),
            Stock INTEGER NOT NULL DEFAULT 0
                CHECK (Stock >= 0),

            FOREIGN KEY (StaffID) REFERENCES Staff(StaffID)
        );
     """)

    cursor.execute("""
        CREATE TABLE CreditCard (
            CardID INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerID INTEGER NOT NULL,

            CardNumber TEXT NOT NULL UNIQUE,
            ExpirationMonth INTEGER NOT NULL
                CHECK (ExpirationMonth BETWEEN 1 AND 12),
            ExpirationYear INTEGER NOT NULL,
            CardholderName TEXT NOT NULL,

            FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
        );
    """)

    cursor.execute("""
        CREATE TABLE Purchase (
            PurchaseID INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerID INTEGER NOT NULL,
            CardID INTEGER NOT NULL,

            PurchaseDate TEXT NOT NULL,

            FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
            FOREIGN KEY (CardID) REFERENCES CreditCard(CardID)
        );
    """)
