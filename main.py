import src.utilities as ut


def main() -> None:
    connection, cursor = ut.init_db_connection()
    ut._create_tables(cursor)
    connection.commit()

    ut.destroy_db_connection(cursor)


if __name__ == "__main__":
    main()
