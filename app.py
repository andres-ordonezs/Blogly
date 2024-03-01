"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "SECRET!"
# debug = DebugToolbarExtension(app)

connect_db(app)

# USER ROUTES


@app.get('/')
def redirect_users():
    """ Redirect to list of all users. """

    return redirect('/users')


@app.get('/users')
def show_users():
    """ Show all users. From here, option to view specific users details or
    navigate to new user form. """

    users = User.query.order_by('first_name').all()

    return render_template(
        'user_listing.html',
        users=users
    )


@app.get('/users/new')
def show_add_form():
    """ Display an add form for new users, with inputs for first name, last name and image URL.
    Upon submission, post data and redirect to user list.   """

    return render_template('user_form.html')


@app.post('/users/new')
def add_new_user():
    """ Process the add form, adding a new user before redirecting back to user list """

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    user = User(first_name=first_name,
                last_name=last_name,
                image_url=image_url
                )

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:user_id>')
def show_user_details(user_id):
    """ Show information about the given user. Takes User's id as URL parameter.
    Includes options to get to their edit page and to delete the user. """

    user = User.query.get_or_404(user_id)

    return render_template("user_detail.html", user=user)


@app.get('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    """ Show the edit page for a user. Takes User's id as URL parameter.
    Displays form with first name, last name and image URL pre-populated with current user data.
    User can cancel to return to the user details page or save to update user data. """

    user = User.query.get_or_404(user_id)

    return render_template('user_edit.html', user=user)


@app.post('/users/<int:user_id>/edit')
def edit_user(user_id):
    """ Process the edit form, returning the user to the /users page.
     Takes User's id as URL parameter. """

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
    """ Delete the user. Takes User's id as URL parameter. """

    user = User.query.get_or_404(user_id)

    db.session.delete(user)

    db.session.commit()

    return redirect('/users')


# POST ROUTES

@app.get('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """ """

    user = User.query.get_or_404(user_id)

    return render_template('new_post_form.html', user=user)


@app.post('/users/<int:user_id>/posts/new')
def handle_add_post(user_id):
    """ """

    title = request.form['title']
    content = request.form['content']
    created_at = None
    user_id = user_id

    post = Post(title=title,
                content=content,
                created_at=created_at,
                user_id=user_id
                )

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.get('/posts/<int:post_id>')
def show_post(post_id):
    """  """

    post = Post.query.get_or_404(post_id)

    return render_template('post.html', post=post)


@app.get('/posts/<int:post_id>/edit')
def show_post_edit_form(post_id):
    """  """

    post = Post.query.get_or_404(post_id)

    return render_template('post_edit.html', post=post)
