from flask import render_template,request,Blueprint, url_for, redirect
from protege.models import Post


core = Blueprint("core", __name__)


@core.route("/", methods=['POST', "GET"])
def index():
    if request.method == "POST":
        keyword = request.form['search']
        return redirect(url_for("posts.video_search", keyword=keyword))
    page = request.args.get('page', 1, type=int)
    videos = Post.query.filter_by(is_leak=1).paginate(page=page, per_page=8)

    all_videos = Post.query.order_by(Post.id).paginate(page=page, per_page=8)

    return render_template("index.html", videos=videos, all_videos=all_videos)