from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from .model import Users


class LoginForm(FlaskForm):
    email = StringField(label="Email: ", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password: ", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegFrom(FlaskForm):
    name = StringField(label="Username: ", validators=[DataRequired()])
    email = StringField(label="Email: ", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password: ", validators=[DataRequired()])
    conf_pass = PasswordField("Confirm Password: ", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

    def validate_email(self, email):
        if Users.query.filter_by(email=email.data).first():
            raise ValidationError("Email has already been registerd")


class UpdateForm(FlaskForm):
    name = StringField(label="Username: ", validators=[DataRequired()])
    email = StringField(label="Email: ", validators=[DataRequired(), Email()])
    pic = FileField("Update Profile Pic", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Update")

    def validate_email(self, email):
        if email.data != current_user.email:
            if Users.query.filter_by(email=email.data).first():
                raise ValidationError("Email has already been registerd")
