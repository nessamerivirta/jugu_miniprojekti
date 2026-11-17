from config import db
from sqlalchemy import text

def create_book(book):
    sql = text("""
        INSERT INTO books
        (citation_key, author, title, publishing_year, publisher)
        VALUES
        (:citation_key, :author, :title, :publishing_year, :publisher)
    """)

    db.session.execute(sql, {
        "citation_key": book.citation_key,
        "author": book.author,
        "title": book.title,
        "publishing_year": book.publishing_year,
        "publisher": book.publisher
    })
    db.session.commit()