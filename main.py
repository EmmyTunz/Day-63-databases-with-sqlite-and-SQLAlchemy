from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Books(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"

db.init_app(app)

with app.app_context():
    db.create_all()


## home page
@app.route('/')
def home():
    result = db.session.execute(db.select(Books).order_by(Books.title))
    all_books = result.scalars()
    print(all_books)
    return render_template('index.html', books=all_books)

# add new book
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        book_name = request.form.get('bookname')
        book_author = request.form.get('bookauthor')
        book_rating = request.form.get('rating')
        book_obj = Books(
            title=book_name,
            author=book_author,
            rating=book_rating
        )
        db.session.add(book_obj)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


# edit book's rating
@app.route("/edit", methods=["GET", "POST"])
def edit():
    book_id = request.args.get('id')
    book = db.session.execute(db.select(Books).where(Books.id == book_id )).scalar()
    if request.method == "POST":
        new_rating = request.form.get('rating')
        book_to_update = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
        book_to_update.rating = new_rating
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", book=book)


# delete book
@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    book = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

