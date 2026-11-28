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
               books.publisher
        FROM references_table
        LEFT JOIN books ON books.reference_id = references_table.id
        ORDER BY references_table.author, references_table.publishing_year
    """)
    return db.session.execute(sql).fetchall()

def get_reference(reference_id):
    sql = text("""
        SELECT references_table.id, type, citation_key, title, author,
               publishing_year, books.publisher
        FROM references_table
        LEFT JOIN books ON books.reference_id = references_table.id
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

def get_update_mainview(json_data):
    author_filter = json_data.get("author", {})
    title_filter = json_data.get("title", {})
    year_filter = json_data.get("publishing_year", {})

    sql = text("""
        SELECT r.id, r.type,
               r.citation_key, r.title,
               r.author, r.publishing_year
        FROM references_table as r
        WHERE
            (:filter_author = 0 OR r.author LIKE :author) AND
            (:filter_title = 0 OR r.title LIKE :title) AND
            (:filter_year = 0 OR r.publishing_year = :publishing_year)
        ORDER BY r.author, r.publishing_year
        """)

    return db.session.execute(sql, {
        "filter_author": author_filter.get("enabled", False),
        "filter_title": title_filter.get("enabled", False),
        "filter_year": year_filter.get("enabled", False),
        "author": f"%{author_filter.get('value', '')}%",
        "title": f"%{title_filter.get('value', '')}%",
        "publishing_year": year_filter.get("value", "")
    }).fetchall()
