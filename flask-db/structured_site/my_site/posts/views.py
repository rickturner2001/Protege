from flask import Flask, Blueprint, redirect, url_for, render_template
from my_site import db
from my_site.posts.forms import AddForm, DelForm
from my_site.models import Post

post_blueprint = Blueprint("posts", __name__, template_folder='templates/posts')

@post_blueprint.route('/')
def index():
    return render_template("index.html")

@post_blueprint.route('/add', methods=['GET', "POST"])
def add():

    form = AddForm()
    if form.validate_on_submit():
        
        title = form.title.data
        text = form.text.data

        new_post = Post(title, text)
        db.session.add(new_post)
        db.session.commit()
 
        return redirect(url_for('posts.list'))

    return render_template("add.html", form=form)

@post_blueprint.route('/list')
def list():

    posts = Post.query.all()
    return render_template("list.html", posts=posts)

@post_blueprint.route('/delete', methods=['GET', "POST"])
def delete():

    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data

        post = Post.query.get(id)
        db.session.delete(post)
        db.session.commit()

        return redirect(url_for("posts.list"))
    
    return render_template("delete.html", form=form)
