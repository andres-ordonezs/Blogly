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
    # TODO: Change default URL
    image_url = input_url if input_url else '<ion-icon name="person-outline"></ion-icon>'

    user = User(first_name=first_name,
                last_name=last_name,
                image_url=image_url
                )

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:user_id>')
def show_user_details(user_id):
    """ """

    user = User.query.get_or_404(user_id)

    return render_template("user_detail.html", user=user)


@app.get('/users/<int:user_id>/edit')
def show_edit_page(user_id):

    user = User.query.get_or_404(user_id)

    return render_template('user_edit.html', user=user)


@app.post('/users/<int:user_id>/edit')
def edit_user(user_id):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User.query.get_or_404(user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):

    user = User.query.get_or_404(user_id)

    db.session.delete(user)

    db.session.commit()

    return redirect('/users')
