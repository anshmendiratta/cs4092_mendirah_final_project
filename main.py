import src.utilities as ut


DB_PATH: str = "ecommerce.db"


def main() -> None:
    connection, cursor = ut.init_db_connection(DB_PATH)
    cursor.execute("PRAGMA foreign_keys = ON;")  # Enable FKs.

    ut.create_tables(connection, cursor)
    ut.insert_values(connection, cursor)

    ut.destroy_db_connection(cursor)


if __name__ == "__main__":
    main()
