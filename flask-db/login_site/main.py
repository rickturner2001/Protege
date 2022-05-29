from my_site import app, db
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user
from my_site.models import User, Post
from my_site.forms import RegistrationForm, LoginForm, AddForm, DelForm

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'post'])
def login():
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("Logged In Succesfully")
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                    next = url_for('index')
            
            return redirect(next)
        
    return render_template("login.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template("register.html", form=form)

@app.route("/add", methods=['GET', 'POST'])
@login_required
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


@app.route("/posts")
def list():

    posts = Post.query.all()
    return render_template("list.html", posts=posts)


@app.route('/delete', methods=['POST', "GET"])
@login_required
def delete():

    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data

        post = Post.query.get(id)
        db.session.delete(post)
        db.session.commit()

        return redirect(url_for("posts.list"))
    
    return render_template("delete.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
