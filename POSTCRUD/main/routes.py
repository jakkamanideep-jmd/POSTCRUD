from flask import Blueprint,request,render_template
from POSTCRUD.models import Post

main=Blueprint("main",__name__)


@main.route("/")
@main.route("/home")
def home():
    page=request.args.get("page",1,type=int)
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(per_page=3,page=page)
    return render_template("home.html",title="home_page",posts=posts)
