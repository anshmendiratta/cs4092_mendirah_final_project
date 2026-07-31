import sqlite3

from typing import List
from pathlib import Path


def init_db_connection(db_path: str) -> [sqlite3.Connection, sqlite3.Cursor]:
    file_path = Path(db_path)

    # Delete DB if already exists to avoid needing to drop tables.
    if file_path.is_file():
        file_path.unlink(missing_ok=True)  # Ignore error if file does not exist.
    else:
        file_path.touch()  # Create if not available.

    connection = sqlite3.connect(db_path)
    return (connection, connection.cursor())


def destroy_db_connection(cursor: sqlite3.Cursor) -> None:
    cursor.close()


def create_tables(connection: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    cursor.executescript("""
        CREATE TABLE Customer (
            CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,

            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE,
            Phone TEXT
        );

        CREATE TABLE Staff (
            StaffID INTEGER PRIMARY KEY AUTOINCREMENT,

            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Position TEXT NOT NULL
        );

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

        CREATE TABLE Purchase (
            PurchaseID INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerID INTEGER NOT NULL,
            CardID INTEGER NOT NULL,

            PurchaseDate TEXT NOT NULL,

            FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
            FOREIGN KEY (CardID) REFERENCES CreditCard(CardID)
        );

        CREATE TABLE PurchaseItem (
            PurchaseID INTEGER NOT NULL,
            ProductID INTEGER NOT NULL,
            Quantity INTEGER NOT NULL
                CHECK (Quantity > 0),
            UnitPrice REAL NOT NULL
                CHECK (UnitPrice >= 0),

            PRIMARY KEY (PurchaseID, ProductID),

            FOREIGN KEY (PurchaseID) REFERENCES Purchase(PurchaseID)
            FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
        );
    """)

    connection.commit()


def insert_values(connection: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    cursor.executescript("""
        INSERT INTO Staff
        (FirstName, LastName, Position)
        VALUES
        ('Alice', 'Johnson', 'Manager'),
        ('Brian', 'Smith', 'Inventory Specialist'),
        ('Carol', 'Lee', 'Sales Associate');

        INSERT INTO Customer
        (FirstName, LastName, Email, Phone)
        VALUES
        ('John', 'Doe', 'john.doe@email.com', '555-123-4567'),
        ('Emma', 'Wilson', 'emma.w@email.com', '555-234-5678'),
        ('Michael', 'Brown', 'michael.b@email.com', '555-345-6789'),
        ('Sophia', 'Davis', 'sophia.d@email.com', '555-456-7890');

        INSERT INTO Product
        (Name, Description, Price, Stock, StaffID)
        VALUES
        ('Mechanical Keyboard', 'RGB mechanical keyboard', 89.99, 25, 2),
        ('Gaming Mouse', 'Wireless gaming mouse', 49.99, 40, 2),
        ('27-inch Monitor', '144Hz IPS monitor', 249.99, 15, 1),
        ('USB-C Hub', '6-port USB-C hub', 39.99, 60, 3),
        ('Webcam', '1080p USB webcam', 69.99, 30, 3);

        INSERT INTO CreditCard
        (CustomerID, CardNumber, ExpirationMonth, ExpirationYear, CardholderName)
        VALUES
        (1, '4111111111111111', 5, 2028, 'John Doe'),
        (1, '5555555555554444', 11, 2027, 'John Doe'),
        (2, '4012888888881881', 8, 2029, 'Emma Wilson'),
        (3, '378282246310005', 3, 2028, 'Michael Brown'),
        (4, '6011111111111117', 9, 2030, 'Sophia Davis');

        INSERT INTO Purchase
        (CustomerID, CardID, PurchaseDate)
        VALUES
        (1, 1, '2026-07-15'),
        (2, 3, '2026-07-16'),
        (1, 2, '2026-07-18'),
        (4, 5, '2026-07-20');

        INSERT INTO PurchaseItem
        (PurchaseID, ProductID, Quantity, UnitPrice)
        VALUES
        (1, 1, 1, 89.99),
        (1, 2, 1, 49.99),

        (2, 3, 2, 249.99),

        (3, 4, 3, 39.99),
        (3, 5, 1, 69.99),

        (4, 2, 2, 49.99),
        (4, 4, 1, 39.99);  
    """)

    connection.commit()
