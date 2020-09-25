# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired

from .models import User


class TribalForm(FlaskForm):
    tribal_attendees = SelectField(
        "Group attending tribal council", validators=[InputRequired()]
    )

    # def __init__(self, *args, **kwargs):
    #     """Create instance."""
    #     super(TribalForm, self).__init__(*args, **kwargs)
    #
    # def validate(self):
    #     """Validate the form."""
    #     initial_validation = super(TribalForm, self).validate()
    #     if not initial_validation:
    #         return False
    #     return True


class RegisterForm(FlaskForm):
    """Register form."""

    first_name = StringField(
        "First Name", validators=[DataRequired(), Length(min=3, max=25)]
    )
    last_name = StringField(
        "Last Name", validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        "Verify password",
        [DataRequired(), EqualTo("password", message="Passwords must match")],
    )

    ## Survivor fields
    game_name = StringField(
        "Game Name", validators=[DataRequired()]
    )
    tribe_name = StringField(
        "Tribe Name", validators=[DataRequired()]
    )
    is_admin = BooleanField(
        "Admin?", validators=[DataRequired()]
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        username_default = self.first_name.data.lower() + self.last_name.data.lower()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=username_default).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True
