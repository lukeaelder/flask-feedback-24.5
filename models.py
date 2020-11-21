from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model."""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, password, email, first, last):
        """Register user and return user."""
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username, password=hashed_utf8, email=email, first_name=first, last_name=last)

    @classmethod
    def authenticate(cls, username, pswd):
        """Validate user and return user."""
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, pswd):
            return user
        else:
            return False

    feedback = db.relationship('Feedback', backref="user", cascade="all, delete-orphan")

class Feedback(db.Model):
    """Feedback model."""
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, db.ForeignKey("users.username"), nullable=False)