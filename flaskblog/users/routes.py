from flaskblog.users.utils import send_reset_mail,save_image
from flask import Blueprint,current_app
from flask import redirect,url_for,request,render_template,flash
from flaskblog import bcrypt,db,mail
from flask_login import login_required,login_user,logout_user,current_user
from flaskblog.users.forms import RegistrationForm,LoginForm,UpdateAccountForm,RequestResetForm,ResetPasswordForm
from flaskblog.models import User,Post
from flask_mail import Message
users=Blueprint("users",__name__)

@users.route("/register",methods=["POST","GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.user"))
    reg_form=RegistrationForm()
    if request.method=="POST":
        if reg_form.validate_on_submit():
            hashed_pw=bcrypt.generate_password_hash(reg_form.password.data).decode("utf-8")
            user1=User(username=reg_form.username.data,email=reg_form.email.data,password=hashed_pw)
            db.session.add(user1)
            db.session.commit()
            return redirect(url_for("users.login"))
        else:
            return render_template("register.html",form=reg_form)    
    else:
        return render_template("register.html",form=reg_form)    


@users.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.user"))    
    form=LoginForm()
    if request.method=="POST":
        if form.validate_on_submit():
            user=User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user,remember=form.remember.data)
                next_page=request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for("users.user"))
            else:
                flash("please check the login details or account does not found")
                return render_template("login.html",form=form)
        else:
            return render_template("login.html",form=form)
    else:
        return render_template("login.html",form=form)


@users.route("/logout")
def logout():
    logout_user()    
    return redirect(url_for("users.login"))


@users.route("/user")
@login_required
def user():
    return render_template("user.html",username=current_user.username,title="userpage")


@users.route("/account",methods=["POST","GET"])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():   
        if form.picture.data:
            picture_file=save_image(form.picture.data)
            current_user.image_file=picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash("your account details has successfully updated")
        return redirect(url_for("users.account"))
    elif request.method == "POST":
        for usr_err in form.username.errors:
            flash(usr_err)
        for email_err in form.email.errors:
            flash(email_err)    
        return redirect(url_for("users.account"))
    elif request.method=="GET":
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file=url_for("static",filename="profile_pic/"+current_user.image_file)
    return render_template("account.html",image_file=image_file,form=form)



@users.route("/user/<username>")
def user_posts(username):
    page=request.args.get("page",1,type=int) 
    user=User.query.filter_by(username=username).first()
    posts=Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=2,page=page)
    return render_template("user_posts.html",posts=posts,user=user)   

@users.route("/reset_request",methods=["POST","GET"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_mail(user)
        flash("your reset mail has been sent checkitout")
    return render_template('reset_request.html',form=form,title="RequestReset")

@users.route("/reset_token/<token>",methods=["POST","GET"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user=User.verify_reset_token(token)
    if user is None:
        flash("your token is either invalid or EXPIRED")
        return redirect(url_for('users.reset_request'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw=bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password=hashed_pw
        db.session.commit()
        flash("your password has been updated")
        return redirect(url_for('users.login'))
    return render_template("reset_token.html",form=form,title='passwordreset')    