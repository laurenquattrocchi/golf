# idea from educativo
# forms module using WTforms for validation & rendering
from flask_wtf import FlaskForm #subclass of form from wtforms library
from wtforms import StringField, PasswordField, IntegerField, SubmitField #wtforms associted classes with field types
from wtforms.validators import InputRequired, Email, EqualTo, Length

#InputRequired() sets required field in HTML
class SignUpForm(FlaskForm):
    first_name = StringField('First Name', 
        validators = [InputRequired(), Length(min=2)])
    last_name = StringField('Last Name', 
        validators = [InputRequired(), Length(min=2)])
    handicap = IntegerField('Handicap', 
        validators = [InputRequired()]) #, Length(max=2)
    email = StringField('Email', 
        validators = [InputRequired(), Email()])
    password = PasswordField('Password', 
        validators = [InputRequired()])
    confirm_password = PasswordField('Confirm Password',
        validators = [InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    submit = SubmitField('Login')

# class AddPlayer(FlaskForm): --???
#     email = StringField('Email',
#                         validators = [InputRequired(), Email()])
#     password = PasswordField('Password', validators = [InputRequired()])
#     submit = SubmitField('Login')