class Inproceeding:
    def __init__(self, citation_key, author, title, proc_year, booktitle):
        self.type = "inproceeding"
        self.citation_key = citation_key
        self.author = author
        self.title = title
        self.publishing_year = proc_year
        self.booktitle = booktitle