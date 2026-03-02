import csv

import pyodbc

def insert_bibs_records(db_cursor: pyodbc.Cursor) -> None:
    # Declare insert query
    insert_query: str = "INSERT INTO bibs VALUES (?)"

    # Open CSV File
    with open("csv_data/bibs.csv", "r") as csv_file:
        csv_reader: csv.DictReader = csv.DictReader(csv_file)
        # Iterate through csv rows
        for row in csv_reader:
            params: list[int] = [
                row["id"]
            ]

            # Execute DB INSERT query
            db_cursor.execute(insert_query, params)

def insert_books_records(db_cursor: pyodbc.Cursor) -> None:
    # Declare insert query
    insert_query: str = "INSERT INTO books VALUES (?, ?, ?, ?, ?)"

    # Open CSV File
    with open("csv_data/books.csv", "r") as csv_file:
        csv_reader: csv.DictReader = csv.DictReader(csv_file)
        # Iterate through csv rows
        for row in csv_reader:
            params: list[int] = [
                row["id"],
                row["publisher"],
                row["title"],
                row["year"],
                row["price"] if row["price"] else None,
            ]

            # Execute DB INSERT query
            db_cursor.execute(insert_query, params)

            insert_bibs_books_record(db_cursor=db_cursor, bib_id=row["bib_id"], book_id=row["id"])

def insert_bibs_books_record(db_cursor: pyodbc.Cursor, bib_id: int, book_id: int) -> None:
    # Declare insert query
    insert_query: str = "INSERT INTO bibs_books VALUES (?, ?)"

    params: list[int] = [
        bib_id,
        book_id
    ]

    # Execute DB INSERT query
    db_cursor.execute(insert_query, params)

def insert_papers_records(db_cursor: pyodbc.Cursor) -> None:
    # Declare insert query
    insert_query: str = "INSERT INTO papers VALUES (?, ?, ?, ?, ?)"

    # Open CSV File
    with open("csv_data/papers.csv", "r") as csv_file:
        csv_reader: csv.DictReader = csv.DictReader(csv_file)
        # Iterate through csv rows
        for row in csv_reader:
            params: list[int] = [
                row["id"],
                row["publisher"],
                row["title"],
                row["year"],
                row["price"] if row["price"] else None,
            ]

            # Execute DB INSERT query
            db_cursor.execute(insert_query, params)

            insert_bibs_papers_record(db_cursor=db_cursor, bib_id=row["bib_id"], paper_id=row["id"])

def insert_bibs_papers_record(db_cursor: pyodbc.Cursor, bib_id: int, paper_id: int) -> None:
    # Declare insert query
    insert_query: str = "INSERT INTO bibs_papers VALUES (?, ?)"

    params: list[int] = [
        bib_id,
        paper_id
    ]

    # Execute DB INSERT query
    db_cursor.execute(insert_query, params)

def insert_authors_records(db_cursor: pyodbc.Cursor) -> None:
    # Declare insert query
    insert_query: str = "INSERT INTO authors VALUES (?, ?, ?, ?)"

    # Open CSV File
    with open("csv_data/authors.csv", "r") as csv_file:
        csv_reader: csv.DictReader = csv.DictReader(csv_file)
        # Iterate through csv rows
        for row in csv_reader:
            params: list[int] = [
                row["id"],
                row["full_name"],
                row["street"] if row["street"] else None,
                row["zip"] if row["zip"] else None,
            ]

            # Execute DB INSERT query
            db_cursor.execute(insert_query, params)

            # Insert books/papers_authors record
            if row["book_id"] != "":
                insert_books_authors_record(db_cursor=db_cursor, book_id=row["book_id"], author_id=row["id"])
            else:
                insert_papers_authors_record(db_cursor=db_cursor, paper_id=row["paper_id"], author_id=row["id"])

def insert_books_authors_record(db_cursor: pyodbc.Cursor, book_id: int, author_id: int) -> None:
    # Declare insert query
    insert_query: str = "INSERT INTO books_authors VALUES (?, ?)"

    params: list[int] = [
        author_id,
        book_id
    ]

    # Execute DB INSERT query
    db_cursor.execute(insert_query, params)

def insert_papers_authors_record(db_cursor: pyodbc.Cursor, paper_id: int, author_id: int) -> None:
    # Declare insert query
    insert_query: str = "INSERT INTO papers_authors VALUES (?, ?)"

    params: list[int] = [
        author_id,
        paper_id
    ]

    # Execute DB INSERT query
    db_cursor.execute(insert_query, params)

def main() -> None:
    # Connect to MYSQL DB running locally
    db_connection: pyodbc.Connection = pyodbc.connect(
        "DRIVER={MySQL ODBC 9.6 Unicode Driver};"
        "SERVER=localhost;"
        "DATABASE=big_data;"
        "UID=root;"
        "PWD=Tiguan2025$;"
    )
    db_cursor: pyodbc.Cursor = db_connection.cursor()

    # Insert records for all tables
    insert_bibs_records(db_cursor)
    insert_books_records(db_cursor)
    insert_papers_records(db_cursor)
    insert_authors_records(db_cursor)

    # Commit transaction
    db_connection.commit()

    # Close connection
    db_connection.close()

if __name__ == "__main__":
    main()
