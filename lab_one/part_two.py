import pyodbc

def main():
    # Connect to MYSQL DB running locally
    db_connection: pyodbc.Connection = pyodbc.connect(
        "DRIVER={MySQL ODBC 9.6 Unicode Driver};"
        "SERVER=localhost;"
        "DATABASE=big_data;"
        "UID=root;"
        "PWD=Tiguan2025$;"
    )
    db_cursor: pyodbc.Cursor = db_connection.cursor()

    # Declare SELECT Statement and execute it
    select_statement: str = "SELECT * FROM lab_one"
    db_response: pyodbc.Cursor = db_cursor.execute(select_statement)

    # Create HTML Page
    html_page: str = """<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    </head>
    <body>
    <h1 class="page-title">
    <span>
    <a id="idm6504896"></a>Collected State of the Union Addresses of U.S. Presidents
    </span>
    </h1>
    <section class="main-section col-sm-12" id="mainaside">
    <div class="toc">
    <p><b>Contents</b></p>
    <dl>
    """

    for db_row in db_response:
        html_page += f"""<dt><span class="article"><a href="{db_row[2]}">{db_row[0]} ({db_row[1]})</a></span></dt>
        """

    html_page += """</dl>
    </div>
    </section>
    </body>
    </html>
    """

    # Write to HTML file
    with open("SimplifiedInfoUnionAddress.html", "w", encoding="utf-8") as f:
        f.write(html_page)

    db_connection.close()


if __name__ == "__main__":
    main()
