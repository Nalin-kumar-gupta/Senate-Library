from datetime import date

from library import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


association_table = db.Table('association',
                             db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                             db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
                             db.Column('ownership_date', db.Date, default=date.today)
                             )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=60), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # for admin user
    # budget = db.Column(db.Integer, nullable=False, default=1000)
    books = db.relationship('Book', secondary=association_table, backref='owners')

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Book(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    author = db.Column(db.String(length=30), nullable=False, default='Unknown')
    # barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    book_count = db.Column(db.Integer(), nullable=False, default=1)
    price = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return f"Book - {self.name}"


class Association(db.Model):
    __table__ = association_table
