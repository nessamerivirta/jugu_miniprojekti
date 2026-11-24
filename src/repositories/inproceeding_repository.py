from config import db
from sqlalchemy import text
from repositories.reference_repository import create_reference

def create_inproceeding(inproceeding):
    create_reference(inproceeding)

    sql = text("""
        INSERT INTO inproceedings
        (reference_id, booktitle)
        VALUES (
        (SELECT id FROM references_table WHERE citation_key =        :citation_key),
        :booktitle
        )
    """)

    db.session.execute(sql, {
        "citation_key": inproceeding.citation_key,
        "booktitle": inproceeding.booktitle
    })
    db.session.commit()

def get_inproceedings():
    sql = text("""
        SELECT
            references_table.id,
            references_table.citation_key,
            references_table.author,
            references_table.title,
            references_table.publishing_year,
            inproceedings.booktitle
        FROM inproceedings
        JOIN references_table
            ON inproceedings.reference_id = references_table.id
        ORDER BY references_table.author,
                 references_table.publishing_year
    """)
    return db.session.execute(sql).fetchall()