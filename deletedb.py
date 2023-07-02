from library import *
from library.models import *

with app.app_context():
    db.drop_all()