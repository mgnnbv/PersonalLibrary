from flask import Blueprint, render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash

from database.models import Book, User
from database.engine import db
from flask_login import login_required, login_user, current_user, logout_user

from forms import LoginForm, RegistrationForm

book_bp = Blueprint('books', __name__)



@book_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('books.profile'))
    return redirect(url_for('books.login'))



@book_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    books = Book.query.all()
    query = ""
    search_results = []


    if request.method == 'POST':
            query = request.form.get('search')  
            if query:
                search_results = Book.query.filter(Book.name.ilike(query)).all()
    
    return render_template('profile.html', 
                           books=books, 
                           user=current_user,
                           query=query,
                           search_results=search_results)




@book_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        author = request.form.get('author')
        year = request.form.get('year')

        book = Book(name=name, description=description, author=author, year=year)
        db.session.add(book)
        db.session.commit()

        flash('Книга успешно добавлена!', 'success')
        return redirect(url_for('books.profile'))

    return render_template('add_book.html')



@book_bp.route('/book/<int:book_id>')
@login_required
def get_book_by_id(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)



@book_bp.route('/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    db.session.delete(book)
    db.session.commit()

    flash('Книга удалена', 'info')
    return redirect(url_for('books.profile'))



@book_bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('books.profile'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            flash('Пользователь не найден. Зарегистрируйтесь.', 'warning')
            return redirect(url_for('books.register'))

        if user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Вы успешно вошли!', 'success')

            next_page = request.args.get('next')
            return redirect(next_page or url_for('books.profile'))

        flash('Неверный пароль', 'danger')

    return render_template('login.html', form=form)


@book_bp.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash('Регистрация успешно завершена! Теперь войдите.', 'success')
        return redirect(url_for('books.login'))

    return render_template('register.html', form=form)


@book_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('books.login'))
