from flask import render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_required, login_user, logout_user, current_user
from project import db
from .forms import RegFrom, LoginForm, UpdateForm
from .model import Users, BlogPost
from project.helper_function import pic_handler

users = Blueprint("users", __name__, template_folder="temlates/users")


@users.route("/register")
def register():
    form = RegFrom()

    if form.validate_on_submit():
        user = Users(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        redirect(url_for("user.login"))
    render_template("register.html", form=form)


@users.route("/login")
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user.checkpassword(form.password.data) and user is not None:
            login_user(user)
            next = request.args.get('next')
            if next == None or next[0] == "/":
                next = url_for("core.index")

            return redirect(next)
    return render_template("login.html", form=form)


@users.route("/logout")
def logout():
    logout_user()


@users.route("/account")
def account():
    form = UpdateForm()

    if form.validate_on_submit():

        if form.pic.data:
            username = current_user.name
            pic = pic_handler(form.pic.data, username)
            current_user.pic = pic

        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for("users.account"))

    elif request.method == "GET":
        form.name.data = current_user.name
        form.email.data = current_user.email

    pic = url_for('static', filename="profile_image/" + current_user.pic)
    return render_template('account.html', pic=pic, form=form)


# users_all_post
@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = Users.query.filter_by(username=username).first_or_404()
    blog_post = BlogPost.query.filter_by(author=user).order_by(BlogPost.pub_date.desc()).pagintae(page=page, per_page=5)
    return render_template("user_blog_post.html", blog_post=blog_post, user = user)
