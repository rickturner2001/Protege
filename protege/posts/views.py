from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import current_user, login_required
from protege import db
from protege.models import Post
from protege.posts.forms import PostForm
from protege import app
from scraper import ph_scraper
import os
from urllib.parse import urlparse
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent  / 'data.sqlite'


posts = Blueprint('posts', __name__)


@posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():

        if urlparse(form.source.data).hostname == 'pornhub.com':
            video_data = ph_scraper(form.source.data)
            print("VIDEO DATA: ")
            print(video_data)
            post = Post(title=form.title.data,
                        post_video_url=form.source.data,
                        post_video=None,
                        category=video_data['categories'][0] if video_data['categories'] else None,
                        thumbnail=video_data['thumbnail'],
                        actors=video_data['actors'][0] if video_data['actors'] else None,
                        user_id=current_user.id
                        )

        else:     
            post = Post(title=form.title.data,
                        post_video_url=form.source.data,
                        user_id=current_user.id,
                        post_video=form.video.data.filename,
                        category=form.category.data,
                        thumbnail=None,
                        actors=None
                        )
            form.video.data.save(os.path.join(
                app.config['UPLOAD_FOLDER'], form.video.data.filename))

        db.session.add(post)
        db.session.commit()
        flash("Post Created")
        return redirect(url_for('core.index'))

    return render_template('create_post.html', form=form)


@posts.route("/videos", methods=['POST', "GET"])
def videos():
    keyword = ""
    query = f"%{keyword}%"
    
    if request.method == "POST":
        
        keyword = request.form['search']
        if keyword:
            return redirect(url_for('posts.video_search',keyword=keyword))
    
    page = request.args.get('page', 1, type=int)
    videos = Post.query.filter(Post.title.like(query)).order_by(Post.id).paginate(page=page, per_page=20)
    return render_template("videos.html", videos=videos, keyword=keyword)


@posts.route("/video_search/<keyword>", methods=['POST', "GET"])
def video_search(keyword):
    if request.method == "POST":
        keyword = request.form['search']
        if keyword:
            return redirect(url_for('posts.video_search',keyword=keyword))

   
    page = request.args.get('page', 1, type=int)
    query = f"%{keyword}%"
    videos = Post.query.filter(Post.title.like(query)).order_by(Post.date.desc()).paginate(page=page, per_page=20)
    return render_template("video_search.html", videos=videos, keyword=keyword)


@posts.route("/category_search/<keyword>", methods=['GET', "POST"])
def category_search(keyword):
    if request.method == "POST":
        if list(request.form.keys())[0] == 'category-search':
            keyword = request.form['category-search']
            return redirect(url_for("posts.category_search", keyword=keyword))
        elif list(request.form.keys())[0] == 'search':
            keyword = request.form['search']
            return redirect(url_for("posts.video_search", keyword=keyword))

    query = f"%{keyword}%"
    page = request.args.get('page', 1, type=int)
    videos = Post.query.filter(Post.category.like(query)).order_by(Post.date.desc()).paginate(page=page, per_page=20)
    return render_template("categories_search.html", videos=videos, keyword=keyword)


@posts.route('/<int:post_id>', methods=["POST", "GET"])
def video(post_id):
    if request.method == "POST":
        keyword = request.form['search']
        if keyword:
            return redirect(url_for('posts.video_search',keyword=keyword))

    video = Post.query.get_or_404(post_id)
    return render_template('video.html', video=video
                           )


@posts.route('/categories', methods=['POST', "GET"])
def categories():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    thumbnails = []

    if request.method == "POST":
        if list(request.form.keys())[0] == 'category-search':
            keyword = request.form['category-search']

            categories = cursor.execute("select distinct category from post where category like ?", (f"%{keyword}%",)).fetchall()
            categories = [c['category'] for c in categories]
            for category in categories:
                thumbnail = cursor.execute("select * from post where category = ?", (category,)).fetchone()['thumbnail']
                thumbnails.append(thumbnail)
            categories = list(set(map(lambda x: x.lower().capitalize(),categories)))
            
            return render_template("categories.html", thumbnails=thumbnails, categories=categories, keyword=keyword)
        
        elif list(request.form.keys())[0] == 'search':
            keyword = request.form['search']
            return(redirect(url_for('posts.video_search', keyword=keyword)))
            


        


    categories = cursor.execute("select distinct category from post order by category").fetchall()
    categories = [c['category'] for c in categories]
    for category in categories:
        thumbnail = cursor.execute("select * from post where category = ?", (category,)).fetchone()['thumbnail']
        thumbnails.append(thumbnail)

    return render_template('categories.html', categories=categories, thumbnails=thumbnails, keyword=None)



