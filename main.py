from flask import Flask, render_template, request, session, redirect

from user import create_user_table, User
from post import create_post_table, Post

import secrets

create_post_table()
create_user_table()

app = Flask("main")
app.secret_key = secrets.token_hex(32)


@app.route("/")
def index_page():
    posts = Post.get_all()

    username = session.get("username", None)
    user = None
    if username:
        user = User.get_user_by_username(username)

    return render_template("index.html", posts=posts, user=user)


@app.route("/registration", methods=["POST", "GET"])
def register_page():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user = User.get_user_by_username(username)
        if user:
            return render_template(
                "register.html", error="Пользователь с таким ником уже есть"
            )

        if password != confirm_password:
            return render_template(
                "register.html", error="Пароли не совпадают"
            )

        User.create(username, password)
        session["username"] = username
        return redirect('/')


@app.route("/logout")
def logout_page():
    del session["username"]
    return redirect('/login')


@app.route("/login", methods=["POST", "GET"])
def login_page():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")

        user = User.get_user_by_username(username)
        if not user:
            return render_template("login.html", error="Неправльный логин или пароль.")

        if user.password == password:
            session["username"] = username
            return redirect('/')
        else:
            return render_template("login.html", error="Неправильный логин или пароль.")


@app.route("/profile", methods=["GET", "POST"])
def profile_page():
    username = session.get("username")

    user = User.get_user_by_username(username)

    if not username:
        return redirect("/login")

    if request.method == "GET":
        posts = Post.get_by_author(user.id)
        return render_template("profile.html", user=user, posts=posts)
    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")

        Post.create(title, text, user.id)
        return redirect('/profile')


@app.route("/profile/<int:id>")
def profile2_page(id: int):
    username = session.get("username")

    user = User.get_user_by_username(username)

    if not username:
        return redirect("/login")
    author = User.get_user_by_id(id)

    posts = Post.get_by_author(id)
    return render_template("postCreatorProfile.html", user=user, author=author, posts=posts)


app.run(host="0.0.0.0", port=8080, debug=True)
