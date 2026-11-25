from flask import redirect, render_template, request, jsonify, flash, Response
from db_helper import reset_db
from repositories.todo_repository import set_done
from config import app, test_env
from repositories.book_repository import create_book, get_books
from repositories.reference_repository import (
    create_reference, get_references, get_reference, update_reference, delete_reference
)
from sqlalchemy.exc import IntegrityError
from repositories.article_repository import create_article, get_articles
from repositories.inproceeding_repository import create_inproceeding, get_inproceedings
from entities.book import Book
from entities.article import Article
from bibtex_export import books_to_bibtex
from entities.inproceeding import Inproceeding

@app.route("/")
def index():
    return redirect("/view_references")

@app.route("/view_references", methods=["GET", "POST"])
def view_references():
    all_references = get_references()
    return render_template("references.html", references=all_references)

@app.route("/view_books", methods=["GET", "POST"])
def view_books():
    all_books = get_books()
    return render_template("books.html", books=all_books)

@app.route("/view_articles", methods=["GET", "POST"])
def view_articles():
    all_articles = get_articles()
    return render_template("articles.html", articles=all_articles)

@app.route("/view_inproceedings", methods=["GET", "POST"])
def view_inproceedings():
    all_inproceedings = get_inproceedings()
    return render_template("inproceedings.html", inproceedings=all_inproceedings)


@app.route("/new_book")
def new_book():
    return render_template("new_book.html")

@app.route("/new_article")
def new_article():
    return render_template("new_article.html")

@app.route("/new_inproceeding")
def new_inproceeding():
    return render_template("new_inproceeding.html")


@app.route("/create_book", methods=["POST"])
def book_creation():
    citation_key = request.form.get("citation_key")
    author = request.form.get("author")
    title = request.form.get("title")
    publishing_year = request.form.get("publishing_year")
    publisher = request.form.get("publisher")

    if not citation_key or not author or not title or not publishing_year or not publisher:
        print("Validation failed!")
        flash("Fill in all the fields")
        return redirect("/new_book")

    book = Book(
        citation_key,
        author,
        title,
        publishing_year,
        publisher
    )

    try:
        # TODO: validate_book(content)
        create_book(book)
        return redirect("/view_references")
    except Exception as error:
        flash(str(error))
        return  redirect("/new_book")

@app.route("/edit_reference/<int:reference_id>", methods=["GET", "POST"])
def edit_reference(reference_id):
    reference = get_reference(reference_id)
    if reference is None:
        return "Reference not found", 404
    if request.method == "POST":
        updated_reference = {
            "type": request.form.get("type", "").strip(),
            "citation_key": request.form.get("citation_key", "").strip(),
            "author": request.form.get("author", "").strip() or None,
            "title": request.form.get("title", "").strip(),
        }
        publishing_year = request.form.get("publishing_year", "").strip()
        publisher = request.form.get("publisher", "").strip()

        if not updated_reference["type"] or not updated_reference["citation_key"] or not updated_reference["title"]:
            flash("Type, citation key, and title are required.")
            return render_template("edit_reference.html", reference=reference), 400

        try:
            updated_reference["publishing_year"] = int(publishing_year) if publishing_year else None
        except ValueError:
            flash("Publishing year must be a number.")
            return render_template("edit_reference.html", reference=reference), 400

        if reference.publisher is not None and not publisher:
            flash("Publisher is required.")
            return render_template("edit_reference.html", reference=reference), 400

        try:
            if not update_reference(
                reference_id,
                updated_reference,
                publisher if reference.publisher is not None else None
            ):
                return "Reference not found", 404
        except IntegrityError:
            flash("A reference with that citation key already exists.")
            return render_template("edit_reference.html", reference=reference), 409

        return redirect("/view_references")

    return render_template("edit_reference.html", reference=reference)
      
@app.route("/create_article", methods=["POST"])
def article_creation():
    citation_key = request.form.get("citation_key")
    author = request.form.get("author")
    title = request.form.get("title")
    journal = request.form.get("journal")
    publishing_year = request.form.get("publishing_year")
    volume = request.form.get("volume")
    pages = request.form.get("pages")

    if not citation_key or not author or not title or not publishing_year or not journal or not volume or not pages:
        print("Validation failed!")
        flash("Fill in all the fields")
        return redirect("/new_article")

    article = Article(
        citation_key,
        author,
        title,
        journal,
        publishing_year,
        volume,
        pages
    )

    try:
        # TODO: validate_article(content)
        create_article(article)
        return redirect("/view_references")
    except Exception as error:
        flash(str(error))
        return  redirect("/new_article")

@app.route("/create_inproceeding", methods=["POST"])
def inproceeding_creation():
    citation_key = request.form.get("citation_key")
    author = request.form.get("author")
    title = request.form.get("title")
    publishing_year = request.form.get("publishing_year")
    booktitle = request.form.get("booktitle")

    if not citation_key or not author or not title or not publishing_year or not booktitle:
        print("Validation failed!")
        flash("Fill in all the fields")
        return redirect("/new_inproceeding")

    inproceeding = Inproceeding(
        citation_key,
        author,
        title,
        publishing_year,
        booktitle
    )

    try:
        # TODO: validate_book(content)
        create_inproceeding(inproceeding)
        return redirect("/view_references")
    except Exception as errorproc:
        flash(str(errorproc))
        return  redirect("/new_inproceeding")
    
@app.route("/delete_reference/<int:reference_id>", methods=["POST"])
def delete_reference_route(reference_id):
    delete_reference(reference_id)
    return redirect("/view_references")

@app.route("/export_bibtex")
def export_bibtex():
    books = get_books()
    content = books_to_bibtex(books)

    return Response(
        content,
        mimetype="text/plain",
        headers={
            "Content-Disposition": "attachment; filename=references.bib"
        }
    )

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
