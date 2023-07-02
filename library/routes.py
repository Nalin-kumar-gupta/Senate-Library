from library import app, db
from flask import render_template, redirect, url_for, flash, request
from library.models import Book, User, Association
from library.forms import RegisterForm, LoginForm, AddNew, AddBook, RemoveBook, EditBook, DeleteBook, RentBook, ReturnBook, PayBill
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
import smtplib


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/books', methods=["GET", "POST"])
@login_required
def book_page():
    # books = [
    #     {'id': 1, 'name': 'Book1', 'barcode': '893212299897', 'price': 500},
    #     {'id': 2, 'name': 'Book2', 'barcode': '123985473165', 'price': 900},
    #     {'id': 3, 'name': 'Book3', 'barcode': '231985128446', 'price': 150}
    # ]
    rented_book_form = RentBook()
    if request.method == "POST":
        rented_book = request.form.get("rented_book")
        rented_book_obj = Book.query.filter_by(name=rented_book).first()
        if rented_book_obj:
            rented_book_obj.book_count -= 1
            Book.query.all()
            rented_book_obj.owners.append(current_user)
            db.session.commit()

            association = Association.query.filter_by(user_id=current_user.id, book_id=rented_book_obj.id).first()

            ownership_date = association.ownership_date
            formatted_date = ownership_date.strftime("%d-%m-%Y")
            db.session.add(association)
            db.session.commit()
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user='nalin.mail.smtp@gmail.com', password='urnpaerrywygejig')
                connection.sendmail(from_addr='nalin.mail.smtp@gmail.com',
                                    to_addrs=current_user.email_address,
                                    msg=f'Subject:NOTICE FOR RENTNG SUCCESSFULLY\n\nDear {current_user.username},\n You have rented {rented_book_obj.name} successfully on {formatted_date}.\n Make sure to return the book before the deadline 10 days')

    books = Book.query.all()

    return render_template('books.html', books=books, rented_book_form=rented_book_form)


@app.route('/register', methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('home_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error creating the user - {err_msg}", category="danger")

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f"Success! You are logged in as: {attempted_user.username}", category='success')
            return redirect(url_for('book_page'))

        else:
            flash("username and password are not match! please try again", category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash(f"You have been logged out!", category='info')
    return redirect(url_for('home_page'))


@app.route('/manage', methods=['GET', 'POST'])
def manage():
    flash(f"Welcome to the Management Section Sir!", category='info')
    add_book_form = AddBook()
    remove_book_form = RemoveBook()
    delete_book_form = DeleteBook()
    edit_book_form = EditBook()
    if request.method == 'POST':
        added_book = request.form.get('added_book')
        removed_book = request.form.get('removed_book')
        deleted_book = request.form.get('deleted_book')
        edited_book = request.form.get('edited_book')
        added_book_obj = Book.query.filter_by(name=added_book).first()
        removed_book_obj = Book.query.filter_by(name=removed_book).first()
        deleted_book_obj = Book.query.filter_by(name=deleted_book).first()
        edited_book_obj = Book.query.filter_by(name=edited_book).first()
        if added_book_obj:
            added_book_obj.book_count += 1
            Book.query.all()
            db.session.commit()

        if removed_book_obj:
            removed_book_obj.book_count -= 1
            Book.query.all()
            db.session.commit()

        if deleted_book_obj:
            deleted_book_obj.book_count = 0
            db.session.delete(deleted_book_obj)
            db.session.commit()

        if edited_book_obj:
            edited_book_obj.name = edit_book_form.book_name.data
            edited_book_obj.author = edit_book_form.author_name.data
            edited_book_obj.price = edit_book_form.book_price.data
            print(edited_book_obj.name)

    books = Book.query.all()
    return render_template('managebooks.html',
                           books=books,
                           add_book_form=add_book_form,
                           remove_book_form=remove_book_form,
                           delete_book_form=delete_book_form,
                           edit_book_form=edit_book_form)


@app.route('/addnew', methods=['GET', 'POST'])
def add_new():
    flash(f"Now you can add a new book to our library!", category='info')
    form = AddNew()
    if form.validate_on_submit():
        book_to_add = Book(name=form.book_name.data,
                           author=form.author_name.data,
                           price=form.book_price.data)
        db.session.add(book_to_add)
        db.session.commit()
        Book.query.all()
        return redirect(url_for('book_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error creating the user - {err_msg}", category="danger")
    return render_template('addnew.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    formatted_current_date = current_date.strftime("%d-%m-%Y")

    books = Book.query.all()
    return_form = ReturnBook()
    if request.method == "POST":
        returned_book = request.form.get("returned_book")
        returned_book_obj = Book.query.filter_by(name=returned_book).first()
        if returned_book_obj:
            returned_book_obj.book_count += 1
            Book.query.all()
            db.session.commit()

            association = Association.query.filter_by(user_id=current_user.id, book_id=returned_book_obj.id).first()
            if association is not None:
                ownership_date = association.ownership_date

                # custom_datetime = datetime(2023, 6, 1)
                # custom_date = custom_datetime.date()
                # time_difference = current_date - custom_date

                formatted_ownership_date = ownership_date.strftime("%d-%m-%Y")
                time_difference = current_date - ownership_date

                num_days = time_difference.days
                money_to_pay = returned_book_obj.price * num_days

                pay_bill_form = PayBill()
                with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user='nalin.mail.smtp@gmail.com', password='urnpaerrywygejig')
                    connection.sendmail(from_addr='nalin.mail.smtp@gmail.com',
                                        to_addrs=current_user.email_address,
                                        msg=f'Subject:NOTICE FOR RETURNING SUCCESSFULLY\n\nDear {current_user.username},\n You have returned{returned_book_obj.name} rented on {formatted_ownership_date} successfully on {formatted_current_date}.')

                returned_book_obj.owners.remove(current_user)
                db.session.commit()

                return render_template('paybill.html',
                                       passed_days=num_days,
                                       ownership_date=formatted_ownership_date,
                                       money_to_pay=money_to_pay,
                                       current_date=formatted_current_date)

    return render_template('profile.html',
                           books=books,
                           return_form=return_form,
                           current_date=formatted_current_date)


