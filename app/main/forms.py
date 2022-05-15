from multiprocessing import context
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired
# from wtfforms.fields.choices import SelectField

class UpdateProfile(FlaskForm):
    bio = TextAreaField("Dear User, please tell us more about you",validators = [InputRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    title = StringField('Comment title :)')
    comment = TextAreaField("Leave a comment here",validators = [InputRequired()])
    submit = SubmitField('Submit')

class BlogForm(FlaskForm):
    category = StringField('Blog Category')
    context = TextAreaField('Enter blog details',validators = [InputRequired()])
    submit = SubmitField('Submit')