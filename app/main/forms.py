from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SubmitField,TextAreaField,SelectField
from wtforms.validators import Required,Email,EqualTo
from wtforms import ValidationError

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Edit bio',validators=[Required()])
    submit = SubmitField('submit')

class PitchNow(FlaskForm):
    title = StringField('Pitch title',validators=[Required()])
    category =SelectField ('Category',choices=[('Business','Business'),('Production','Production'),('Interview','Interview'),('Promotion','Promotion'),('Sales','Sales'),('Marketing','Marketing')],validators=[Required()])
    description = TextAreaField('Pitch my idea',validators=[Required()])
    submit = SubmitField('submit')

class MyComment(FlaskForm):
    comment = TextAreaField('Your comment',validators=[Required()])
    submit = SubmitField('submit')

class UpVote(FlaskForm):
    upvote = SubmitField('submit')

class DownVote(FlaskForm):
    downvote = SubmitField('submit')