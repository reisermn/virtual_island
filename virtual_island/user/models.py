# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin

from virtual_island.database import (
    Column,
    PkModel,
    db,
    reference_col,
    relationship,
    backref
)
from virtual_island.extensions import bcrypt

# # Association class to link User and Game. It's not actually part of our model, and it updates itself
user_game = db.Table(
    'user_game',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('games.id'))
)


class Role(PkModel):
    """A role for a user."""

    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col("users", nullable=True)
    user = relationship("User", backref="roles")

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"


class Game(PkModel):
    """A game of 20 contestants managed by an admin."""

    __tablename__ = "games"
    name = Column(db.String(80), unique=True, nullable=False)
    # players is the backref
    # players = db.relationship('User', secondary='user_game') #, backref=db.backref('seasons'))

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Game({self.name})>"


class User(UserMixin, PkModel):
    """A user of the app."""

    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.LargeBinary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    full_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    # Survivor-specific variables
    seasons = db.relationship('Game', secondary=user_game, backref=db.backref('players'), lazy='dynamic')
    # To update, use game.players.append(userObject)
    tribe_name = Column(db.String(30), nullable=True)
    fire = Column(db.Boolean(), default=True)
    jury = Column(db.Boolean(), default=False)
    tribal = Column(db.Boolean(), default=False)
    votes = Column(db.Integer, default=0)
    round = Column(db.Integer, default=0)

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        super().__init__(username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"


class Tribal(PkModel):
    """A role for a user."""

    __tablename__ = "tribal"
    tribal_tribe_name = Column(db.String(80), unique=True, nullable=False)

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Tribal({self.name})>"


### Examples

## Many to Many - many users can subscribe to many channels
# class User(PkModel):
#     user_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20))
#     subscriptions = db.relationship('Channel', secondary=subs, backref=db.backref('subscribers', lazy='dynamic'))
#
# class Channel(db.Model):
#     channel_id = db.Column(db.Integer, primary_key=True)
#     channel_name = db.Column(db.String(20))
#
# # We need an association table to link these 2. It's not actually part of our model and it updates itself
# subs = db.Table(
#     'subs',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
#     db.Column('channel_id', db.Integer, db.ForeignKey('channel.channel_id'))
# )
#
# # To add subscriptions:
# channel1.subscribers.append(user1)
# db.session.commit()
#
# # Query
# for user in channel1.subscribers: print(user.name)


## One to Many - one owner has multiple pets
# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20))
#     pets = db.relationship('Pet', backref='owner')
#
# class Pet(db.Model)
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20))
#     owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))
#
# # To add people
# matt = Person(name='Matt')
# spot = Pet(name='Spot', owner=matt)
# olive = Pet(name='Olive', owner=matt)
#
# matt.pets
# matt.pets[0]
# matt.pets[0].name
#
# olive.owner.name
