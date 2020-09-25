# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, login_user, logout_user

from virtual_island.extensions import login_manager
from virtual_island.public.forms import LoginForm
from virtual_island.user.forms import RegisterForm
from virtual_island.user.models import User, Game
from virtual_island.utils import flash_errors

from ..extensions import db

blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    login_form = LoginForm(request.form)
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        if login_form.validate_on_submit():
            login_user(login_form.user)
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for("user.games")
            return redirect(redirect_url)
        else:
            flash_errors(login_form)
    return render_template("public/home.html", login_form=login_form)


@blueprint.route("/logout/")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.home"))


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # If game doesn't exist, create it
        game_instance = Game.query.filter_by(name=form.game_name.data).first()
        if game_instance is None:
            Game.create(name=form.game_name.data)
            game_instance = Game.query.filter_by(name=form.game_name.data).first()

        # create a default username
        username_default = form.first_name.data.lower() + form.last_name.data.lower()
        full_name_default = form.first_name.data + form.last_name.data
        User.create(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            full_name=full_name_default,
            username=username_default,
            email=form.email.data,
            password=form.password.data,
            active=True,
            tribe_name=form.tribe_name.data,
            is_admin=form.is_admin.data
        )
        # Add the user to the correct game
        user_instance = User.query.filter_by(username=username_default).first() # get the user we just created
        game_instance.players.append(user_instance)
        db.session.commit() # DON'T FUCKING FORGET TO COMMIT

        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form)


@blueprint.route("/about/")
def about():
    """About page."""
    login_form = LoginForm(request.form)
    return render_template("public/about.html", login_form=login_form)
