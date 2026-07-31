import src.utilities as ut


def main() -> None:
    connection, cursor = ut.init_db_connection()

    cursor.execute("PRAGMA foreign_keys = ON;")  # Enable FKs.

    ut.destroy_tables(cursor)
    connection.commit()

    ut.create_tables(cursor)
    connection.commit()

    ut.destroy_db_connection(cursor)


if __name__ == "__main__":
    main()
