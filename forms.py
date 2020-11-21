from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length

class RegisterForm(FlaskForm):
    """Form for registering a user."""
    username = StringField("Username", 
        validators=[InputRequired(message="Username cannot be blank"), Length(max=20, message="Username must be less than 20 characters")])
    password = PasswordField("Password", 
        validators=[InputRequired(message="Password cannot be blank")])
    email = StringField("Email", 
        validators=[InputRequired(message="Email cannot be blank"), Email(message="Invalid email"), Length(max=50, message="Email must be less than 50 characters")])
    first_name = StringField("First Name", 
        validators=[InputRequired(message="First name cannot be blank"), Length(max=30, message="First name must be less than 20 characters")])
    last_name = StringField("Last Name", 
        validators=[InputRequired(message="Last name cannot be blank"), Length(max=30, message="Last name must be less than 20 characters")])

class LoginForm(FlaskForm):
    """Form for loging in a user."""
    username = StringField("Username", 
        validators=[InputRequired(message="Username cannot be blank"), Length(max=20, message="Username must be less than 20 characters")])
    password = PasswordField("Password", 
        validators=[InputRequired(message="Password cannot be blank")])

class FeedbackForm(FlaskForm):
    """Form for adding feedback."""
    title = StringField("Title", 
        validators=[InputRequired(message="Title cannot be blank"), Length(max=100, message="Title must be less than 100 characters")])
    feedback = TextAreaField("Feedback", 
        validators=[InputRequired(message="Feedback cannot be blank")])