"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post
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
Post.query.delete()
# Add users
user1 = User(first_name='Whiskey', last_name="dog")
user2 = User(first_name='Bowser', last_name="dog")
user3 = User(first_name='Spike', last_name="porcupine")
# Add posts
print("USERIDDDDD ---->", user1.id)
# Add new objects to session, so they'll persist
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

db.session.commit()

# post1 = Post(title="Post1", content="Post1 Content", user_id=1)
# post2 = Post(title="Post2", content="Post2 Content", user_id=2)
# post3 = Post(title="Post3", content="Post3Content", user_id=2)

# db.session.add(post1)
# db.session.add(post2)
# db.session.add(post3)

# Commit--otherwise, this never gets saved!
# db.session.commit()

# print("POSTTTTTT ---->", Post.query.all())


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
    return render_template('user_add.html')


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
    posts = user.posts
    return render_template("user_detail.html", user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show edit page for a user"""
    user = User.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)


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


@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def add_post_form(user_id):
    return render_template("post_add.html")


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    title = request.form['title']
    content = request.form['content']
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>', methods=['GET'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    print("POSTTTT---->", Post.query.all())
    return render_template("post_detail.html", post=post)


@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def edit_post(post_id):
    post1 = Post.query.get_or_404(post_id)
    post = {
        "title": post1.title,
        "content": post1.content,
        "id": post1.id
    }
    return render_template("post_edit.html", post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()
    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=['GET'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/users")


@app.route('/posts')
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)