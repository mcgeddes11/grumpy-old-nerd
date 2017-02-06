from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, SubmitField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(Form):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me',default=False)

class ForgotPasswordForm(Form):
    email = StringField('email', validators=[DataRequired(), Email()])

class PasswordResetForm(Form):
    password = PasswordField("password",validators=[DataRequired(),Length(min=8,max=50), EqualTo("confirm_password", message="Passwords must match")])
    confirm_password = PasswordField("confirm_password")

class AddUserForm(Form):
    email = StringField('email', validators=[DataRequired(), Email(message="Invalid email")])
    password = PasswordField('password', validators=[DataRequired()])
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    urole = StringField('urole', validators=[DataRequired()])

class PostForm(Form):
    title = TextAreaField("Enter a title", validators=[DataRequired()])
    body = PageDownField("Your post here", validators=[DataRequired()])
    save_draft = SubmitField("save_draft")
    publish = SubmitField("publish")

class EditPostForm(Form):
    id = StringField('id', validators=[DataRequired()])
    title = TextAreaField("title", validators=[DataRequired()])
    body = PageDownField("body", validators=[DataRequired()])
    save_draft = SubmitField("save_draft")
    publish = SubmitField("publish")

class ContactMeForm(Form):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email(message="Invalid email")])
    message = TextAreaField("message", validators=[DataRequired()])
    send = SubmitField("send")
