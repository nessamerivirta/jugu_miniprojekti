from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.todo_repository import set_done
from config import app, test_env
from repositories.book_repository import create_book, get_books
from repositories.reference_repository import create_reference, get_references, delete_reference
from entities.book import Book

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

@app.route("/new_book")
def new_book():
    return render_template("new_book.html")

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


@app.route("/delete_reference/<int:reference_id>", methods=["POST"])
def delete_reference_route(reference_id):
    delete_reference(reference_id)
    return redirect("/view_references")
    

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
