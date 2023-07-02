from wtforms import StringField, PasswordField, SubmitField, IntegerField
from flask_wtf import FlaskForm
from wtforms.validators import Length, EqualTo, DataRequired, Email, ValidationError
from library.models import User, Book


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exists!! Please try a different username")

    def validate_email(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError("Email address already exists try logging in!")

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=5, max=30), DataRequired()])
    password2 = PasswordField(label='Confirm password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class AddNew(FlaskForm):

    def validate_book_name(self, name_to_check):
        book = Book.query.filter_by(name=name_to_check.data).first()
        if book:
            raise ValidationError("Book already exists!! you can increase the stock in manage books")

    book_name = StringField(label='Book Name:', validators=[DataRequired()])
    author_name = StringField(label='Author Name:')
    book_price = IntegerField(label='$ price / day:', validators=[DataRequired()])
    submit = SubmitField(label='Add Book')


class AddBook(FlaskForm):
    submit = SubmitField(label='Add')


class RemoveBook(FlaskForm):
    submit = SubmitField(label='Remove')


class DeleteBook(FlaskForm):
    submit = SubmitField(label='Delete')


class EditBook(FlaskForm):
    book_name = StringField(label='Book Name:', validators=[DataRequired()])
    author_name = StringField(label='Author Name:')
    book_price = IntegerField(label='$ price / day:', validators=[DataRequired()])
    submit = SubmitField(label='Edit')


class RentBook(FlaskForm):
    rent_days = IntegerField(label='days', validators=[DataRequired()])
    submit = SubmitField(label='Rent')


class ReturnBook(FlaskForm):
    submit = SubmitField(label='Return')


class PayBill(FlaskForm):
    submit = SubmitField(label='Pay')