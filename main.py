# NOTE:
# The assignment mentioned that you *can* make this interactive
# using the terminal/console, but I am choosing not to for simplicity.
# This program can be trivially modified to become a fully-fledged
# command-line interface which parses the user's input, but there
# would be no change in the "business logic" after parsing, so I think
# it suffices to just hardcode some of the possible commands a user may
# enter.

import src.utilities as ut


DB_PATH: str = "ecommerce.db"


def main() -> None:
    # Init

    connection, cursor = ut.init_db_connection(DB_PATH)
    cursor.execute("PRAGMA foreign_keys = ON;")  # Enable FKs.

    ut.create_tables(connection, cursor)
    ut.insert_values(connection, cursor)

    # SQL Queries.

    # List all products.
    print("=== ALL PRODUCTS [Name, Price, Stock] ===")
    ut.pretty_print_query(cursor, "SELECT Name, Price, Stock FROM Product;")

    print("=== CUSTOMERS WITH # CREDIT CARDS > 1 [First, Last, # Cards] ===")
    ut.pretty_print_query(
        cursor,
        """
            SELECT
                Customer.FirstName,
                Customer.LastName,
                COUNT(CreditCard.CardID) AS NumberOfCards
            FROM Customer
            JOIN CreditCard
                ON Customer.CustomerID = CreditCard.CustomerID
            GROUP BY Customer.CustomerID
            HAVING COUNT(CreditCard.CardID) > 1;
        """,
    )

    print("=== POPULAR PRODUCTS [Name, Units Sold] ===")
    ut.pretty_print_query(
        cursor,
        """
        SELECT
            Product.Name,
            SUM(PurchaseItem.Quantity) AS UnitsSold
        FROM Product
        JOIN PurchaseItem
            ON Product.ProductID = PurchaseItem.ProductID
        GROUP BY Product.ProductID
        ORDER BY UnitsSold DESC
        """,
    )

    # Cleanup.

    ut.destroy_db_connection(cursor)


if __name__ == "__main__":
    main()
