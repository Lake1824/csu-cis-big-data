import csv
# The Python standard library includes an XML parser that supports DOM
import xml.dom.minidom
from _elementtree import Element
from dataclasses import dataclass
from xml.dom.minicompat import NodeList
from xml.dom.minidom import Document

@dataclass
class Author:
    full_name: str
    street: str | None = None
    zip: str | None = None

    def __init__(self, author_dom_element: Element) -> None:
        if first_name_elements := author_dom_element.getElementsByTagName("first-name"):
            if last_name_elements := author_dom_element.getElementsByTagName("last-name"):
                self.full_name = first_name_elements[0].firstChild.nodeValue.strip() + " " + last_name_elements[0].firstChild.nodeValue.strip()
        elif name_elements := author_dom_element.getElementsByTagName("name"):
            self.full_name = name_elements[0].firstChild.nodeValue[1:-1]
        else:
            self.full_name = author_dom_element.firstChild.nodeValue[1:-1]

        if address_dom_elements := author_dom_element.getElementsByTagName("address"):
            self.street = address_dom_elements[0].getElementsByTagName("street")[0].firstChild.nodeValue[1:-1]
            self.zip = address_dom_elements[0].getElementsByTagName("zip")[0].firstChild.nodeValue[1:-1]

@dataclass
class Book:
    publisher: str
    authors: list[Author]
    title: str
    year: int
    price: int | None = None

    def __init__(self, book_dom_element: Element) -> None:
        self.publisher = book_dom_element.getElementsByTagName("publisher")[0].firstChild.nodeValue[1:-1]
        self.title = book_dom_element.getElementsByTagName("title")[0].firstChild.nodeValue[1:-1]
        self.year = int(book_dom_element.getElementsByTagName("year")[0].firstChild.nodeValue[1:-1])
        self.price = int(book_dom_element.getAttribute("price")) if book_dom_element.getAttribute("price") else None

        author_dom_elements: NodeList[Element] = book_dom_element.getElementsByTagName("author")
        self.authors = [
            Author(
                author_dom_element=author_dom_element
            )
            for author_dom_element in author_dom_elements
        ]

@dataclass
class Paper:
    publisher: str
    authors: list[Author]
    title: str
    year: int
    price: int | None = None

    def __init__(self, paper_dom_element: Element) -> None:
        self.publisher = paper_dom_element.getElementsByTagName("publisher")[0].firstChild.nodeValue[1:-1]
        self.title = paper_dom_element.getElementsByTagName("title")[0].firstChild.nodeValue[1:-1]
        self.year = int(paper_dom_element.getElementsByTagName("year")[0].firstChild.nodeValue[1:-1])
        self.price = int(paper_dom_element.getAttribute("price")) if paper_dom_element.getAttribute("price") else None

        author_dom_elements: NodeList[Element] = paper_dom_element.getElementsByTagName("author")
        self.authors = [
            Author(
                author_dom_element=author_dom_element
            )
            for author_dom_element in author_dom_elements
        ]

@dataclass
class Bib:
    books: list[Book]
    papers: list[Paper]

    def __init__(self, bib_dom_element: Element) -> None:
        book_dom_elements: NodeList[Element] = bib_dom_element.getElementsByTagName("book")
        self.books = [
            Book(book_dom_element=book_dom_element)
            for book_dom_element in book_dom_elements
        ]

        paper_dom_elements: NodeList[Element] = bib_dom_element.getElementsByTagName("paper")
        self.papers = [
            Paper(paper_dom_element=paper_dom_element)
            for paper_dom_element in paper_dom_elements
        ]

def main() -> None:
    # Get DOM Tree for input XML file
    dom_tree: Document = xml.dom.minidom.parse("./input_file.xml")

    # Get bib DOM elements
    bib_dom_elements: NodeList[Element] = dom_tree.getElementsByTagName("bib")

    # Create dataclass representations of the XML elements within the bib_dom_elements node list
    bibs: list[Bib] = [
        Bib(bib_dom_element=bib_dom_element)
        for bib_dom_element in bib_dom_elements
    ]

    # Create CSV file outputs for the bibs data
    create_csv_files_for_bibs(bibs=bibs)

def create_csv_files_for_bibs(bibs: list[Bib]) -> None:
    # Create bibs CSV
    create_bibs_csv(bibs=bibs)

    # Create books CSV
    create_books_csv(bibs=bibs)

    # Create papers CSV
    create_papers_csv(bibs=bibs)

    # Create authors CSV
    create_authors_csv(bibs=bibs)

def create_bibs_csv(bibs: list[Bib]) -> None:
    file_name: str = "csv_data/bibs.csv"
    fieldnames: list[str] = ["id"]
    with open(file_name, "w", newline="") as csv_file:
        csv_writer: csv.DictWriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for id, _ in enumerate(bibs):
            csv_writer.writerow(
                {
                    "id": id + 1,
                }
            )

def create_books_csv(bibs: list[Bib]) -> None:
    file_name: str = "csv_data/books.csv"
    fieldnames: list[str] = ["id", "publisher", "title", "year", "price", "bib_id"]
    with open(file_name, "w", newline="") as csv_file:
        csv_writer: csv.DictWriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        book_id_counter: int = 1

        for bib_id, bib in enumerate(bibs):
            for book in bib.books:
                csv_writer.writerow(
                    {
                        "id": book_id_counter,
                        "publisher": book.publisher,
                        "title": book.title,
                        "year": book.year,
                        "price": book.price,
                        "bib_id": bib_id + 1,
                    }
                )

                book_id_counter += 1

def create_papers_csv(bibs: list[Bib]) -> None:
    file_name: str = "csv_data/papers.csv"
    fieldnames: list[str] = ["id", "publisher", "title", "year", "price", "bib_id"]
    with open(file_name, "w", newline="") as csv_file:
        csv_writer: csv.DictWriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        paper_id_counter: int = 1

        for bib_id, bib in enumerate(bibs):
            for paper in bib.papers:
                csv_writer.writerow(
                    {
                        "id": paper_id_counter,
                        "publisher": paper.publisher,
                        "title": paper.title,
                        "year": paper.year,
                        "price": paper.price,
                        "bib_id": bib_id + 1,
                    }
                )

                paper_id_counter += 1

def create_authors_csv(bibs: list[Bib]) -> None:
    file_name: str = "csv_data/authors.csv"
    fieldnames: list[str] = ["id", "full_name", "street", "zip", "book_id", "paper_id"]
    with open(file_name, "w", newline="") as csv_file:
        csv_writer: csv.DictWriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        book_id_counter: int = 1
        paper_id_counter: int = 1
        author_id_counter: int = 1

        for bib in bibs:
            for book in bib.books:
                for author in book.authors:
                    csv_writer.writerow(
                        {
                            "id": author_id_counter,
                            "full_name": author.full_name,
                            "street": author.street,
                            "zip": author.zip,
                            "book_id": book_id_counter,
                            "paper_id": None,
                        }
                    )
                    author_id_counter += 1
                book_id_counter += 1

            for paper in bib.papers:
                for author in paper.authors:
                    csv_writer.writerow(
                        {
                            "id": author_id_counter,
                            "full_name": author.full_name,
                            "street": author.street,
                            "zip": author.zip,
                            "book_id": None,
                            "paper_id": paper_id_counter,
                        }
                    )
                    author_id_counter += 1
                paper_id_counter += 1

if __name__ == "__main__":
    main()
