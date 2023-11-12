"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from models import db, connect_db, User

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    """Show home page with links"""
    return render_template('home.html')

@app.route('/users')
def user_listing():
    """Show links for each user and the add user form"""
    users = User.query.all()
    return render_template('user_listing.html', users=users)

@app.route('/users/new')
def new_user_form():
    """Show add new user form"""
    return render_template('new_user_form.html')

@app.route('/users/new', methods=["POST"])
def new_user_form_submit():
    """Add new user to db using inputs from form"""
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]
    image_url = image_url if image_url else None
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<user_id>')
def user_detail(user_id):
    """Show details for a given user"""
    user = User.query.get(user_id)
    return render_template('user_detail.html', user=user)

@app.route('/users/<user_id>/edit')
def user_edit_form(user_id):
    """"Show form to edit an existing user"""
    user = User.query.get(user_id)
    return render_template('user_edit.html', user=user)

@app.route('/users/<user_id>/edit', methods=["POST"])
def user_edit_form_submit(user_id):
    """"Show form to edit an existing user"""
    user = User.query.get(user_id)
    
    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    image_url = request.form["image-url"]
    user.image_url = image_url if image_url else None

    db.session.add(user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete a user from the database"""
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
