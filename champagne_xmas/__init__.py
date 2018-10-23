from flask import Flask
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ce2878bbd3b851fccf0a22304cc1f46c'
bcrypt = Bcrypt(app)

from champagne_xmas import routes