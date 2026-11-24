from config import db
from sqlalchemy import text
from repositories.reference_repository import create_reference

def create_book(book):
    create_reference(book)

    sql = text("""
        INSERT INTO books
        (reference_id, publisher)
        VALUES (
        (SELECT id FROM references_table WHERE citation_key = :citation_key), :publisher
        )
    """)

    db.session.execute(sql, {
        "citation_key": book.citation_key,
        "publisher": book.publisher
    })
    db.session.commit()

def get_books():
    sql = text("""
        SELECT
            references_table.id,
            references_table.citation_key,
            references_table.author,
            references_table.title,
            references_table.publishing_year,
            books.publisher
        FROM books
        JOIN references_table
            ON books.reference_id = references_table.id
        ORDER BY references_table.author,
                 references_table.publishing_year
    """)
    return db.session.execute(sql).fetchall()