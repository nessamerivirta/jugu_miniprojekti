from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.todo_repository import get_todos, set_done
from config import app, test_env
from repositories.book_repository import create_book, get_books, delete_book
from entities.book import Book

@app.route("/")
def index():
    return redirect("/view_books")

@app.route("/new_book")
def new_book():
    return render_template("new_book.html") # TODO: create html

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
        return redirect("/view_books")
    except Exception as error:
        flash(str(error))
        return  redirect("/new_book")

@app.route("/view_books", methods=["GET", "POST"])
def view_books():
    all_books = get_books()
    return render_template("books.html", books=all_books)

@app.route("/toggle_todo/<todo_id>", methods=["POST"])
def toggle_todo(todo_id):
    set_done(todo_id)
    return redirect("/")

@app.route("/delete_book/<int:book_id>", methods=["POST"])
def delete_book_route(book_id):
    delete_book(book_id)
    return redirect("/view_books")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
