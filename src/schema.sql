CREATE TABLE books (
  id INTEGER PRIMARY KEY,
  citation_key TEXT NOT NULL UNIQUE,
  author TEXT NOT NULL,
  title TEXT NOT NULL,
  publishing_year INTEGER NOT NULL,
  publisher TEXT NOT NULL
);

CREATE TABLE articles (
  id INTEGER PRIMARY KEY,
  citation_key TEXT NOT NULL UNIQUE,
  author TEXT NOT NULL,
  title TEXT NOT NULL,
  journal TEXT NOT NULL,
  publishing_year INTEGER NOT NULL,
  volume TEXT NOT NULL,
  pages TEXT NOT NULL
);