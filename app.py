from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "supersecretkey"

connect_db(app)

@app.route("/")
def home_page():
    """Redirect to /register."""
    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register_page():
    """Show register form and handle register user."""
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first = form.first_name.data
        last = form.last_name.data
        new_user = User.register(username, password, email, first, last)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError as e:
            err = str(e)
            if "users_username_key" in err:
                form.username.errors = ["Username already taken, please try another"]
            if "users_email_key" in err:
                form.email.errors = ["Email already in use, please try another"]
            return render_template("register.html", form=form)
        session["user_username"] = new_user.username
        flash("Successfully registered", "success")
        return redirect(f"/users/{new_user.username}")
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login_page():
    """Show login form and handle loging in user."""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            session['user_username'] = user.username
            flash("successfully logged in", "success")
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username or password"]
    return render_template("login.html", form=form)

@app.route("/users/<username>")
def user_page(username):
    """Show user page."""
    if 'user_username' not in session:
        flash("You must login", "warning")
        return redirect("/login")
    sessuser = session["user_username"]
    user = User.query.filter_by(username=username).first()
    feedback = Feedback.query.filter_by(username=username).all()
    if user.username == session["user_username"]:
        return render_template("user.html", user=user, feedback=feedback)
    return redirect(f"/users/{sessuser}")
    
@app.route("/logout")
def logout_user():
    """Logout a user."""
    if 'user_username' not in session:
        flash("You must login", "warning")
        return redirect("/login")
    session.pop('user_username')
    flash("Succesfully logged out", "success")
    return redirect("/login")

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    if 'user_username' not in session:
        flash("You must login", "warning")
        return redirect("/login")
    sessuser = session["user_username"]
    user = User.query.filter_by(username=username).first()
    if user.username == session["user_username"]:
        db.session.delete(user)
        db.session.commit()
        session.pop('user_username')
        flash("Successfully deleted user", "success")
        return redirect("/")
    flash("You dont have permission to do that", "danger")
    return redirect(f"/users/{sessuser}")

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    if 'user_username' not in session:
        flash("You must login", "warning")
        return redirect("/login")
    sessuser = session["user_username"]
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.feedback.data
        new_feedback = Feedback(title = title, content = content, username = username)
        db.session.add(new_feedback)
        try:
            db.session.commit()
        except IntegrityError as e:
            err = str(e)
            if "feedback_title_key" in err:
                form.title.errors = ["Title cannot be blank"]
            if "feedback_feedback_key" in err:
                form.feedback.errors = ["Feedback cannot be blank"]
        flash("Successfully created feedback", "success")
        return redirect(f"/users/{username}")
    if username == session["user_username"]:
        return render_template("feedback.html", form = form)
    flash("You dont have permission to do that", "danger")
    return redirect(f"/users/{sessuser}")

@app.route("/feedback/<int:id>/update", methods=["POST", "GET"])
def edit_feedback(id):
    if 'user_username' not in session:
        flash("You must login", "warning")
        return redirect("/login")
    sessuser = session["user_username"]
    form = FeedbackForm()
    feedback = Feedback.query.get(id)
    if form.validate_on_submit():
        title = form.title.data
        content = form.feedback.data
        feedback.title = title
        feedback.content = content
        db.session.add(feedback)
        try:
            db.session.commit()
        except IntegrityError as e:
            err = str(e)
            if "feedback_title_key" in err:
                form.title.errors = ["Title cannot be blank"]
            if "feedback_feedback_key" in err:
                form.feedback.errors = ["Feedback cannot be blank"]
        flash("Successfully edited feedback", "success")
        return redirect(f"/users/{sessuser}")
    if sessuser == feedback.username:
        form.title.data = feedback.title
        form.feedback.data = feedback.content
        return render_template("editfeedback.html", form = form)
    flash("You dont have permission to do that", "danger")
    return redirect(f"/users/{sessuser}")

@app.route("/feedback/<int:id>/delete", methods=["POST"])
def delete_feedback(id):
    feedback = Feedback.query.get(id)
    sessuser = session["user_username"]
    if feedback.username == session["user_username"]:
        db.session.delete(feedback)
        db.session.commit()
        flash("Successfully deleted feedback", "success")
        return redirect(f"/users/{sessuser}")
    flash("You dont have permission to do that", "danger")
    return redirect(f"/users/{sessuser}")

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors with invalid URL."""
    flash("Invalid URL, 404 error", "danger")
    return redirect("/register")