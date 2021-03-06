from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


'migerate'
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')

from app import views, models


