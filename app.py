
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "lovely17"
db = SQLAlchemy(app)

import routes
import models

with app.app_context():
    db.create_all()
    




if __name__ == "__main__":
    app.run()
