import datetime
from project import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140))
    pic = db.Column(db.String(200), default="default.png", nullable=True)
    email = db.Column(db.String(140), unique=True, index=True)
    password = db.Column(db.String(140))
    posts = db.relationship("BlogsPost", backref="author", lazy=True)

    def __init__(self, name, email, password, **kwargs):
        super().__init__(kwargs)
        self.username = name
        self.email = email
        self.password = generate_password_hash(password)

    def pass_check(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User {self.username}"

class BlogPost(db.Model):
    id = db.Column(db.Integer())
    user_id = db.Column(db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(140), nullable=False)
    pub_date = db.Column(db.DATETIME(), default=datetime.utcnow , nullable=False)
    text = db.Column(db.TEXT(), nullable=False)

    def __repr__(self):
        return f"Post {self.title} "