from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

@app.route('/')
def book_list():
    books = Book.query.all()
    return render_template('book_list.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        new_book = Book(title=title, author=author, year=year)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('book_list'))
    return render_template('add_book.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)