from config import db
from sqlalchemy import text
from repositories.reference_repository import create_reference

def create_article(article):
    create_reference(article)

    sql = text("""
        INSERT INTO articles
        (reference_id, journal, volume, pages)
        VALUES (
        (SELECT id FROM references_table WHERE citation_key = :citation_key),
          :journal, :volume, :pages
        )
    """)

    db.session.execute(sql, {
        "citation_key": article.citation_key,
        "journal": article.journal,
        "volume": article.volume,
        "pages": article.pages
    })
    db.session.commit()

def get_articles():
    sql = text("""
        SELECT
            references_table.id,
            references_table.citation_key,
            references_table.author,
            references_table.title,
            references_table.publishing_year,
            articles.journal,
            articles.volume,
            articles.pages
        FROM articles
        JOIN references_table
            ON articles.reference_id = references_table.id
        ORDER BY references_table.author,
                 references_table.publishing_year
    """)
    return db.session.execute(sql).fetchall()