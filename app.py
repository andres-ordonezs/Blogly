"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.get('/')
def redirect_users():
    """ #TODO: """

    return redirect('/users')


@app.get('/users')
def show_users():
    """ #TODO: """

    return render_template(
        'user_listing.html',
        users=User.query.all()
    )


@app.get('/users/new')
def show_add_form():
    """  """
    return render_template('user_form.html')


@app.post('/users/new')
def add_new_user():
    """  """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    input_url = request.form['image_url']
    image_url = input_url if input_url else '<ion-icon name="person-outline"></ion-icon>'

    user = User(first_name=first_name,
                last_name=last_name,
                image_url=image_url
                )

    db.session.add(user)
    db.session.commit()

    return redirect('/users')
