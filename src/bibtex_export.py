def book_to_bibtex(book):
    return (
        f"@book{{{book.citation_key},\n"
        f"    author = {{{book.author}}},\n"
        f"    title = {{{book.title}}},\n"
        f"    year = {{{book.publishing_year}}},\n"
        f"    publisher = {{{book.publisher}}}\n"
        "}"
    )

def books_to_bibtex(books):
    return "\n\n".join(book_to_bibtex(book) for book in books)