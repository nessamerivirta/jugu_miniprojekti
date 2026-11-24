class Article:
    def __init__(self, citation_key, author, title, journal, publishing_year, volume, pages):
        self.type = "article"
        self.citation_key = citation_key
        self.author = author
        self.title = title
        self.journal = journal
        self.publishing_year = publishing_year
        self.volume = volume
        self.pages = pages