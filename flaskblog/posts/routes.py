from flask import Blueprint,flash,redirect,url_for,render_template,abort,request
from flaskblog import db
from flask_login import login_user,logout_user,login_required,current_user
from flaskblog.posts.forms import Postform
from flaskblog.models import Post,User 
posts=Blueprint("posts",__name__)

@posts.route("/post/new",methods=["POST","GET"])
@login_required
def new_post():
    form=Postform()
    if form.validate_on_submit():
        post=Post(title=form.title.data, content=form.content.data,author=current_user) #why author =current_user means now the post even have the userdata/registerdata 
        db.session.add(post)
        db.session.commit()
        flash("your post has been succesfully created")
        return redirect(url_for("main.home"))
    return render_template("create_post.html",title="new_post",form=form,legend="new post")

@posts.route("/post/<post_id>")
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template("post.html",post=post)


@posts.route('/post/<int:post_id>/update',methods=["POST","GET"])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form=Postform()

    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash("post got updated")
        return redirect(url_for("posts.post",post_id=post.id))
    elif request.method=="GET":
        form.title.data=post.title
        form.content.data=post.content
    return render_template("update_post.html",title="updatepost",form=form,legend="update post",post=post)


@posts.route("/post/<post_id>/delete>")
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("our post got DELETED!!")
    return redirect(url_for('main.home'))
    

@posts.route("/user/<username>")
def user_posts(username):
    page=request.args.get("page",1,type=int) 
    user=User.query.filter_by(username=username).first()
    posts=Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=2,page=page)
    return render_template("user_posts.html",posts=posts,user=user)   