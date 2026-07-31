import click as c
import click_shell as cs

import src.utilities as ut

from typing import List, Dict, Optional


REQUIRED_FIELDS: Dict[str, List[str]] = {
    "Customer": ["CustomerID", "FirstName", "LastName", "Email", "Phone"],
    "Staff": ["StaffID", "FirstName", "LastName", "Position"],
    "Product": ["ProductID", "StaffID", "Name", "Description", "Price", "Stock"],
    "CreditCard": [
        "CardID",
        "CustomerID",
        "CardNumber",
        "ExpirationMonth",
        "ExpirationYear",
        "CardholderName",
    ],
    "Purchase": ["PurchaseID", "CustomerID", "CardID", "PurchaseDate"],
    "PurchaseItem": ["PurchaseID", "ProductID", "Quantity", "UnitPrice"],
}

REQUIRED_FIELDS_TYPES: Dict[str, List[type]] = {
    "Customer": [int, str, str, str, str],
    "Staff": [int, str, str, str],
    "Product": [int, int, str, str, float, int],
    "CreditCard": [int, int, str, int, int, str],
    "Purchase": [int, int, int, str],
    "PurchaseItem": [int, int, int, float],
}

DB_PATH: str = "ecommerce.db"

connection, cursor = ut.init_db_connection(DB_PATH)
cursor.execute("PRAGMA foreign_keys = ON;")  # Enable FKs.


def _cleanup(cc: Optional[c.Context]) -> None:
    ut.destroy_db_connection(cursor)


# App. Needs not functionality on its own.
@cs.shell(prompt="> ", intro="CS4092 Final Project CLI", on_finished=_cleanup)
def _cli():
    ut.create_tables(connection, cursor)
    ut.insert_values(connection, cursor)


@_cli.command()
def help() -> None:
    print("""
Available commands:
- `list` (lists all available tables)
- `view` table (lists all rows)
- `select` (from a specific table)
- `insert` (specify values to fill into a table)
""")


@_cli.command()
def list() -> None:
    ALL_TABLES: List[str] = [
        "Customer",
        "Staff",
        "Product",
        "CreditCard",
        "Purchase",
        "PurchaseItem",
    ]

    for idx, table in enumerate(ALL_TABLES):
        print(f"{idx + 1}. {table}")


@_cli.command()
def view() -> None:
    table_name = str(input("Which table would you like to list? ")).strip()

    print(f"=== {table_name} ===")

    cursor.execute(f"SELECT * FROM {table_name}")
    for row in cursor.fetchall():
        print(row)


@_cli.command()
def insert() -> None:
    table_name = input("Insert into which table? ").strip()

    required_input: List[str] = REQUIRED_FIELDS[f"{table_name}"]
    user_data: List[any] = []

    print("HELP")

    for idx, req in enumerate(required_input):
        user_input = input(f"{req}: ").strip()
        required_type: type = REQUIRED_FIELDS_TYPES[f"{table_name}"][idx]
        user_data.append(required_type(user_input))

    print("HELP")

    columns = ", ".join(required_input)
    placeholders = ", ".join(["?"] * len(user_data))

    cursor.execute(
        f"""
        INSERT INTO {table_name}
            ({columns})
        VALUES
            ({placeholders})
        """,
        user_data,
    )
