#coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask_pagedown.fields import PageDownField

class NameForm(FlaskForm):
	name = StringField('UserName', validators = [Required()])
	password = PasswordField('Password', validators = [Required()])
	rememberme = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
	name = StringField('Username', validators=[
		validators.Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
										  'Usernames must have only letters, '
										  'numbers, dots or underscores')])
	password = PasswordField('Password', validators=[
		Required(), EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('Register')

class ChangePasswordForm(FlaskForm):
	old_password = PasswordField('Old password', validators=[Required()])
	password = PasswordField('New password', validators=[
		Required(), EqualTo('password2', message='Passwords must match')])
	password2 = PasswordField('Confirm new password', validators=[Required()])
	submit = SubmitField('Update Password')

class EditProfileForm(FlaskForm):
	name = StringField('Real name', validators = [Length(0, 64)])
	location = StringField('Location', validators = [Length(0, 64)])
	aboutMe = StringField('About me')
	submit = SubmitField('Submit')

class PostForm(FlaskForm):
	content = PageDownField('Content', validators = [Length(0, 500), Required()])
	submit = SubmitField('Submit')

class CommentForm(FlaskForm):
	body = PageDownField('评论', validators = [Length(0, 500), Required()])
	submit = SubmitField('Submit')