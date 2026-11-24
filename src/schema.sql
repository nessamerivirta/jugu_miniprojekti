PRAGMA foreign_keys = ON;

CREATE TABLE references_table (
  id INTEGER PRIMARY KEY,
  type TEXT NOT NULL,
  citation_key TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL,
  author TEXT,
  publishing_year INTEGER
);

CREATE TABLE books (
  id INTEGER PRIMARY KEY,
  reference_id INTEGER NOT NULL UNIQUE
    REFERENCES references_table(id) ON DELETE CASCADE,
  publisher TEXT NOT NULL
);