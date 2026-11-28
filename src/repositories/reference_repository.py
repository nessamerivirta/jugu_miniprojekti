from config import db
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

def create_reference(reference):
    sql = text("""
            INSERT INTO references_table
            (type, citation_key, author, title, publishing_year)
            VALUES
            (:type, :citation_key, :author, :title, :publishing_year)
        """)

    db.session.execute(sql, {
            "type": reference.type,
            "citation_key": reference.citation_key,
            "author": reference.author,
            "title": reference.title,
            "publishing_year": reference.publishing_year
        })
    db.session.commit()

def get_references():
    sql = text("""
        SELECT references_table.id, references_table.type,
               references_table.citation_key, references_table.title,
               references_table.author, references_table.publishing_year,
               books.publisher,
               articles.journal, articles.volume, articles.pages,
               inproceedings.booktitle
        FROM references_table
        LEFT JOIN books ON books.reference_id = references_table.id
        LEFT JOIN articles ON articles.reference_id = references_table.id
        LEFT JOIN inproceedings ON inproceedings.reference_id = references_table.id
        ORDER BY references_table.author, references_table.publishing_year
    """)
    return db.session.execute(sql).fetchall()

def get_reference(reference_id):
    sql = text("""
        SELECT references_table.id, type, citation_key, title, author,
               publishing_year, books.publisher,
               articles.journal, articles.volume, articles.pages,
               inproceedings.booktitle
        FROM references_table
        LEFT JOIN books ON books.reference_id = references_table.id
        LEFT JOIN articles ON articles.reference_id = references_table.id
        LEFT JOIN inproceedings ON inproceedings.reference_id = references_table.id
        WHERE references_table.id = :reference_id
        """)
    return db.session.execute(sql, {"reference_id": reference_id}).fetchone()

def update_reference(reference_id, reference, publisher=None):
    sql = text("""
        UPDATE references_table
        SET type = :type,
            citation_key = :citation_key,
            author = :author,
            title = :title,
            publishing_year = :publishing_year
        WHERE id = :reference_id
    """)
    try:
        result = db.session.execute(sql, {
            "reference_id": reference_id,
            "type": reference["type"],
            "citation_key": reference["citation_key"],
            "author": reference["author"],
            "title": reference["title"],
            "publishing_year": reference["publishing_year"]
        })

        if result.rowcount == 0:
            db.session.rollback()
            return False

        if publisher is not None:
            db.session.execute(text("""
                UPDATE books
                SET publisher = :publisher
                WHERE reference_id = :reference_id
            """), {"reference_id": reference_id, "publisher": publisher})

        if "journal" in reference:
            db.session.execute(text("""
                UPDATE articles
                SET journal = :journal,
                    volume = :volume,
                    pages = :pages
                WHERE reference_id = :reference_id
            """), {
                "reference_id": reference_id,
                "journal": reference["journal"],
                "volume": reference["volume"],
                "pages": reference["pages"],
            })

        if "booktitle" in reference:
            db.session.execute(text("""
                UPDATE inproceedings
                SET booktitle = :booktitle
                WHERE reference_id = :reference_id
            """), {
                "reference_id": reference_id,
                "booktitle": reference["booktitle"],
            })

        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise

    return True

def delete_reference(reference_id):
    sql = text("""
        DELETE FROM references_table
        WHERE id = :reference_id
    """)
    db.session.execute(sql, {"reference_id": reference_id})
    db.session.commit()