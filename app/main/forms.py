from wtforms import validators
from wtforms.fields.core import StringField
from app.models import Blog
from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField,SelectField
from wtforms.validators import Required


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')


class BlogForm(FlaskForm):
    title=StringField('Title',validators=[Required()])
    category = SelectField('Category', choices=[('Social Events','Social Events'),('Festivals','Festivals'),('Concerts','Concerts')],validators=[Required()])
    post = TextAreaField('Your Blog', validators=[Required()])
    submit = SubmitField('Blog')

class CommentForm(FlaskForm):
    comment = TextAreaField('Leave a comment',validators=[Required()])
    submit = SubmitField('Comment')