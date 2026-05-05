from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import ValidationError,DataRequired,Email,EqualTo,Length
from flask_wtf.file import FileField,FileAllowed
from flaskblog.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username=StringField("username",name="usrname",validators=[DataRequired(),Length(min=5,max=20)],render_kw={"autocomplete":"None"})
    email=StringField("email",name="email",validators=[DataRequired(),Email()])
    password=PasswordField("password",name="password",validators=[DataRequired()],render_kw={"autocomplete":"new-password"})
    confirm_password=PasswordField("confrim_password",name="confirm_password",validators=[DataRequired(),EqualTo("password")],render_kw={"autocomplete":"new-password"})
    submit=SubmitField("submit")
    remember=BooleanField("rememberme")

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("the username already exist please try another one")
        
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first() 
        if user:
            raise ValidationError("email already exist")  


class LoginForm(FlaskForm):
    username=StringField("username",validators=[DataRequired(),Length(min=5,max=20)],render_kw={"autocomplete":"username"})
    password=PasswordField("password",validators=[DataRequired()],render_kw={"autocomplete":"current-password"})
    submit=SubmitField("login")  
    remember=BooleanField("rememberme")  


class UpdateAccountForm(FlaskForm):
    username=StringField("username",name="usrname",validators=[DataRequired(),Length(min=5,max=20)])
    email=StringField("email",name="email",validators=[DataRequired(),Email()])
    picture=FileField("picture",validators=[FileAllowed("jpg","png")])
    submit=SubmitField("update")    


    def validate_username(self,username):
        if current_user != username.data:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("the username already exist please try another one")
        
    def validate_email(self,email):
        if current_user != email.data:
            user=User.query.filter_by(email=email.data).first() 
            if user:
                raise ValidationError("email already exist")  



class RequestResetForm(FlaskForm):
    email=StringField("email",validators=[DataRequired(),Email()])
    submit=SubmitField("request_for_reset")
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            return ValidationError("the email is not valid")

class ResetPasswordForm(FlaskForm):
    Password=PasswordField("password",validators=[DataRequired()])
    confirm_password=PasswordField("confirm_password",validators=[DataRequired(),EqualTo(Password)])
    submit=SubmitField("send_mail")

