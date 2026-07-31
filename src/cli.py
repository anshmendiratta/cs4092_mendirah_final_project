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


# Main app. Contains startup code.
@cs.shell(prompt="> ", intro="CS4092 Final Project CLI", on_finished=_cleanup)
def _cli() -> None:
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

    print()


@_cli.command()
def view() -> None:
    table = str(input("Which table would you like to list? ")).strip()
    print()

    print(f"=== {table} ===")

    cursor.execute(f"SELECT * FROM {table};")
    for row in cursor.fetchall():
        print(row)

    print()


@_cli.command()
def select() -> None:
    table: str = input("Select from which table? ").strip()
    attributes: List[str] = REQUIRED_FIELDS[f"{table}"]

    selected_attributes: List[str] = (
        input(
            f"""You may select from the following attributes: {attributes}. If you wish to select several, simply separate the desired columns by a comma.
Attributes: """
        )
        .replace(" ", "")
        .split(",")
    )
    print()

    cursor.execute(f"SELECT {','.join(selected_attributes)} FROM {table};")

    print(f"=== {table} {selected_attributes} ===")
    for row in cursor.fetchall():
        print(row)

    print()


@_cli.command()
def insert() -> None:
    table: str = input("Insert into which table? ").strip()
    print()

    required_input: List[str] = REQUIRED_FIELDS[f"{table}"]
    user_data: List[any] = []

    for idx, req in enumerate(required_input):
        user_input = input(f"{req}: ").strip()
        required_type: type = REQUIRED_FIELDS_TYPES[f"{table}"][idx]
        user_data.append(required_type(user_input))

    columns = ", ".join(required_input)
    placeholders = ", ".join(["?"] * len(user_data))

    cursor.execute(
        f"""
        INSERT INTO {table}
            ({columns})
        VALUES
            ({placeholders});
        """,
        user_data,
    )

    print("Inserted.")
    print()
