from flask_wtf import Form
from wtforms import TextAreaField, SubmitField

class CreatePostForm(Form):
    post = TextAreaField("Note: ")
    submit = SubmitField("Submit")
