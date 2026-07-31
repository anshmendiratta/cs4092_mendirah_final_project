import utilities as ut


def main() -> None:
    cursor = ut.init_db_connection()
    ut._create_tables(cursor)

    ut.destroy_db_connection(cursor)


if __name__ == "__main__":
    main()
