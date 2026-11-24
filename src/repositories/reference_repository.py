from config import db
from sqlalchemy import text

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
        SELECT id, type, citation_key, title, author, publishing_year
        FROM references_table
        ORDER BY author, publishing_year
    """)
    return db.session.execute(sql).fetchall()

def delete_reference(reference_id):
    sql = text("""
        DELETE FROM references_table
        WHERE id = :reference_id
    """)
    db.session.execute(sql, {"reference_id": reference_id})
    db.session.commit()