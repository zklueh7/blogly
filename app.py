"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from models import db, connect_db, User, Post

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
    """Update user info using inputs from form"""
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

@app.route('/users/<user_id>/posts/new')
def new_post_form(user_id):
    """Show the form to add a new post for a given user"""
    user = User.query.get(user_id)
    return render_template('new_post_form.html', user=user)

@app.route('/users/<user_id>/posts/new', methods=["POST"])
def new_post_form_submit(user_id):
    """Submit new post to database"""
    user = User.query.get(user_id)
    title = request.form["title"]
    content = request.form["content"]
    new_post = Post(title=title, content=content, user_id=user_id)
    
    db.session.add(new_post)
    db.session.commit()

    return render_template('user_detail.html', user=user)

@app.route('/posts/<post_id>')
def show_post(post_id):
    """Show a post for post_id"""
    post = Post.query.get(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/posts/<post_id>/edit')
def post_edit_form(post_id):
    """Show form to edit post"""
    post = Post.query.get(post_id)
    return render_template('post_edit_form.html', post=post)

@app.route('/posts/<post_id>/edit', methods=["POST"])
def post_edit_form_submit(post_id):
    """Submit post edits to database"""
    post = Post.query.get(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    db.session.add(post)
    db.session.commit()
    return render_template('post_detail.html', post=post)

@app.route('/posts/<post_id>/delete')
def delete_post(post_id):
    """Delete a post"""
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect('/')
