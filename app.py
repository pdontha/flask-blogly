"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pudutha'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
user1 = User(first_name='Whiskey', last_name="dog")
user2 = User(first_name='Bowser', last_name="dog")
user3 = User(first_name='Spike', last_name="porcupine")

# Add new objects to session, so they'll persist
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

# Commit--otherwise, this never gets saved!
db.session.commit()


@app.route('/')
def home():
    return redirect('/users')


@app.route('/users')
def list_users():
    """List all existing users """
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/new')
def show_add():
    """Show add form"""
    return render_template('add.html')


@app.route('/users/new', methods=["POST"])
def add_user():
    """Add user and redirect to list"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show selected user details"""
    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show edit page for a user"""
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Update user and redirect to list"""
    user = User.query.get_or_404(user_id) 
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form['img_url']
    db.session.commit()
    return redirect("/")


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete user and redirect to list"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")
