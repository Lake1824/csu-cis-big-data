import csv
import os
from csv import DictReader
from typing import Final

import requests
from lxml import html
from lxml.html import HtmlElement
import pyodbc
from requests import Response

# Declare some constants
BASE_URL: Final[str] = "https://www.presidency.ucsb.edu"
LIST_OF_SPEECHES_URL_PATH: Final[str] = "/documents/app-categories/spoken-addresses-and-remarks/presidential/state-the-union-addresses?items_per_page=101"
LOCAL_SPEECHES_DIRECTORY_NAME: Final[str] = "state_the_union_addresses"
CSV_FILE_NAME: Final[str] = "part_one_data.csv"
CSV_FILE_FIELD_NAMES: Final[list[str]] = ["name_of_president", "date_of_union_address", "link_to_address", "filename_address", "text_of_address"]

def create_csv_file_with_speech_data() -> None:
    # Get main page DOM tree carrying URL paths to all speeches
    list_of_speeches_response: Response = requests.get(BASE_URL + LIST_OF_SPEECHES_URL_PATH)
    list_of_speeches_dom_tree: HtmlElement = html.fromstring(list_of_speeches_response.content)

    # Get URL paths of all speeches
    url_paths_to_speeches: list[str] = list_of_speeches_dom_tree.xpath('//div[@class="view-content"]//div[@class="field-title"]/p/a/@href')
    # Start a counter for txt file naming purposes
    speech_counter: int = 1

    # Create a csv file to read from when seeding the DB table
    with open(CSV_FILE_NAME, "w") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=CSV_FILE_FIELD_NAMES)
        csv_writer.writeheader()

        # Iterate through speeches
        for path in url_paths_to_speeches:
            # Get DOM tree for speech
            speech_response: Response = requests.get(BASE_URL + path)
            speech_dom_tree: HtmlElement = html.fromstring(speech_response.content)

            # Pull out the president's name, the date the speech was given and the full speech
            president_name: str = speech_dom_tree.xpath('//div[@class="col-sm-8 "]/div[@class="field-docs-person"]//h3[@class="diet-title"]/a/text()')[0]
            date_of_speech: str = speech_dom_tree.xpath('//div[@class="field-docs-start-date-time"]/span/text()')[0]

            speech_elements: list[HtmlElement] = speech_dom_tree.xpath('//div[@class="field-docs-content"]/p')
            # Some speeches had italic tags <i></i> with text in addition to normal paragraphs <p></p>
            # In those cases I wanted to grab both texts. The speeches looked funky just grabbing the paragraphs without the italic tags
            full_speech: str = '\n'.join(speech_element.text_content() for speech_element in speech_elements)

            # Write the speech to a txt file
            full_speech_file_name: str = f"{LOCAL_SPEECHES_DIRECTORY_NAME}/address{speech_counter}.txt"
            with open(full_speech_file_name, "w") as text_file:
                text_file.write(full_speech)

            # Write csv row
            csv_writer.writerow(
                {
                    "name_of_president": president_name,
                    "date_of_union_address": date_of_speech,
                    "link_to_address": BASE_URL + path,
                    "filename_address": full_speech_file_name,
                    "text_of_address": full_speech
                }
            )

            speech_counter += 1

def seed_lab_one_mysql_table_with_csv_file_data() -> None:
    # Connect to MYSQL DB running locally
    db_connection: pyodbc.Connection = pyodbc.connect(
        "DRIVER={MySQL ODBC 9.6 Unicode Driver};"
        "SERVER=localhost;"
        "DATABASE=big_data;"
        "UID=root;"
        "PWD=Tiguan2025$;"
    )
    db_cursor: pyodbc.Cursor = db_connection.cursor()

    # Declare insert query
    insert_query: str = "INSERT INTO lab_one VALUES (?, ?, ?, ?, ?)"

    # Open CSV File
    with open(CSV_FILE_NAME, "r") as csv_file:
        csv_reader: DictReader = csv.DictReader(csv_file)
        # Iterate through csv rows
        for row in csv_reader:
            # Create params list of speech data
            params: list[str] = [
                row[CSV_FILE_FIELD_NAMES[0]],
                row[CSV_FILE_FIELD_NAMES[1]],
                row[CSV_FILE_FIELD_NAMES[2]],
                row[CSV_FILE_FIELD_NAMES[3]],
                row[CSV_FILE_FIELD_NAMES[4]],
            ]
            # Execute DB INSERT query
            db_cursor.execute(insert_query, params)
            # Commit transaction
            db_connection.commit()

    db_connection.close()


if __name__ == "__main__":
    # We dont want to keep generating the csv file every run if we dont have too
    if not os.path.exists(CSV_FILE_NAME):
        create_csv_file_with_speech_data()
        print(f"CSV file {CSV_FILE_NAME} created")

    # Check if the csv file exists before seeding db
    if os.path.exists(CSV_FILE_NAME):
        seed_lab_one_mysql_table_with_csv_file_data()
        print("Lab 1 DB table seeded")
