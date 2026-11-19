from config import db
from sqlalchemy import text

def get_references():
    sql = text("""
        SELECT id, title, type
        FROM books
        ORDER BY author, publishing_year
    """)
    return db.session.execute(sql).fetchall()