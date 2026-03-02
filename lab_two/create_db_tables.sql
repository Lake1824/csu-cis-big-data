CREATE TABLE bibs(
    id INTEGER NOT NULL PRIMARY KEY
);

CREATE TABLE books(
    id INTEGER NOT NULL PRIMARY KEY,
    publisher VARCHAR(25) NOT NULL,
    title TEXT NOT NULL,
    year INTEGER NOT NULL,
    price INTEGER
);

CREATE TABLE papers(
    id INTEGER NOT NULL PRIMARY KEY,
    publisher VARCHAR(25) NOT NULL,
    title TEXT NOT NULL,
    year INTEGER NOT NULL,
    price INTEGER
);

CREATE TABLE authors(
    id INTEGER NOT NULL PRIMARY KEY,
    full_name VARCHAR(25) NOT NULL,
    street VARCHAR(50),
    zip TINYTEXT
);

CREATE TABLE bibs_books(
    bib_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    PRIMARY KEY (bib_id, book_id),
    FOREIGN KEY (bib_id) REFERENCES bibs (id),
    FOREIGN KEY (book_id) REFERENCES books (id)
);

CREATE TABLE bibs_papers(
    bib_id INTEGER NOT NULL,
    paper_id INTEGER NOT NULL,
    PRIMARY KEY (bib_id, paper_id),
    FOREIGN KEY (bib_id) REFERENCES bibs (id),
    FOREIGN KEY (paper_id) REFERENCES papers (id)
);

CREATE TABLE books_authors(
    author_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    PRIMARY KEY (author_id, book_id),
    FOREIGN KEY (author_id) REFERENCES authors (id),
    FOREIGN KEY (book_id) REFERENCES books (id)
);

CREATE TABLE papers_authors(
    author_id INTEGER NOT NULL,
    paper_id INTEGER NOT NULL,
    PRIMARY KEY (author_id, paper_id),
    FOREIGN KEY (author_id) REFERENCES authors (id),
    FOREIGN KEY (paper_id) REFERENCES papers (id)
);
