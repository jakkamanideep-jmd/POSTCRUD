from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

class Postform(FlaskForm):
    title=StringField("title",validators=[DataRequired()])
    content=StringField("content",validators=[DataRequired()])
    submit=SubmitField("post")