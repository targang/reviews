import datetime

from flask import redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app import app, db
from app.models import Review, User


@app.route("/")
@login_required
def index():
    return render_template(
        "index.html",
        reviews=Review.query.all(),
    )


@app.route("/answer", methods=["POST"])
def answer():
    data = request.json
    id_ = data["id"]
    answer = data["answer"]
    review = Review.query.get(int(id_))
    review.answer = answer
    db.session.commit()


@app.route("/create_review", methods=["GET", "POST"])
def create_review():
    if request.method == 'GET':
        return render_template('create_review.html')
    username = request.form['username']
    text = request.form['text']
    stars = int(request.form['stars'])
    date = datetime.date.fromisoformat(request.form['date'])
    url = request.form['url']
    review = Review(username=username, text=text, stars=stars, date=date, url=url)
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        login = request.form.get("login")
        password = request.form.get("password")

        user = User.query.filter_by(login=login).first()

        if not user or password != user.password:
            return render_template("login.html", invalid=True)

        login_user(user, remember=True)
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))
