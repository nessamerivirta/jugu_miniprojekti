from config import db
from sqlalchemy import text

def create_article(article):
    sql = text("""
        INSERT INTO articles
        (citation_key, author, title, journal, publishing_year, volume, pages)
        VALUES
        (:citation_key, :author, :title, :journal, :publishing_year, :volume, :pages)
    """)

    db.session.execute(sql, {
        "citation_key": article.citation_key,
        "author": article.author,
        "title": article.title,
        "publishing_year": article.publishing_year,
        "publisher": article.publisher
    })
    db.session.commit()

def get_articles():
    sql = text("""
        SELECT id, citation_key, author, title, journal, publishing_year, volume, pages
        FROM articles
        ORDER BY author, publishing_year
    """)
    return db.session.execute(sql).fetchall()

def delete_article(article_id):
    sql = text("""
        DELETE FROM articles
        WHERE id = :article_id
    """)
    db.session.execute(sql, {"article_id": article_id})
    db.session.commit()