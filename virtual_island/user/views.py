# -*- coding: utf-8 -*-
"""User views."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from virtual_island.user.models import User, Game


blueprint = Blueprint("user", __name__, url_prefix="/seasons", static_folder="../static")


@blueprint.route("/")
@login_required
def games():
    """List members."""

    current_user
    game_list = Game.query.all()

    context = {
        'current_user': current_user,
        'games': game_list
    }

    return render_template("users/seasons.html", **context)


@blueprint.route('/<game_name>', methods=['GET', 'POST'])
@login_required
def game(game_name):
    # if not current_user.admin:
    #     return redirect(url_for('public.home'))

    game_selected = Game.query.filter_by(name=game_name).first()
    player_list = User.query.filter(User.seasons.any(Game.name == game_name)).order_by(User.tribe_name.desc()).all() # Uses the relationship to perform the filter

    # if request.method == 'POST':
    #     question.answer = request.form['answer']
    #     db.session.commit()
    #
    #     return redirect(url_for('main.unanswered'))

    context = {
        'game_selected': game_selected,
        'player_list': player_list
    }

    return render_template('users/season_home.html', **context)

    def edit_user(request, id):
        user = User.query.get(id)
        form = UserDetails(request.POST, obj=user)
        form.group_id.choices = [(g.id, g.name) for g in Group.query.order_by('name')]
