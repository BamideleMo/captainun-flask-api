from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    fullname=db.Column(db.Text,nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    country=db.Column(db.Text,nullable=False)
    group=db.Column(db.Text,nullable=False)
    username=db.Column(db.Text, unique=True, nullable=False)
    password=db.Column(db.Text, nullable=False)
    status = db.Column(db.Text,default='unverified')
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    def __repr__(self) -> str:
        return 'Users>>>{self.username}'

class Country(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    country_name=db.Column(db.Text,nullable=False)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    def __repr__(self) -> str:
        return 'Country>>>{self.country_name}'


class State(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    state_country=db.Column(db.Text,nullable=False)
    state_name=db.Column(db.Text,nullable=False)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    def __repr__(self) -> str:
        return 'State>>>{self.state_name}'


class City(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    city_country=db.Column(db.Text,nullable=False)
    city_state=db.Column(db.Text,nullable=False)
    city_name=db.Column(db.Text,nullable=False)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    def __repr__(self) -> str:
        return 'City>>>{self.city_name}'


class Organization(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    organization_country=db.Column(db.Text,nullable=False)
    organization_state=db.Column(db.Text,nullable=False)
    organization_city=db.Column(db.Text,nullable=False)
    organization_name=db.Column(db.Text,nullable=False)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    def __repr__(self) -> str:
        return 'Organization>>>{self.organization_name}'

class Goals(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    goal_for=db.Column(db.Integer,nullable=False)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    def __repr__(self) -> str:
        return 'Rating>>>{self.goal_id}'


class Rating(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    rating_value=db.Column(db.Integer,nullable=False)
    goal_id=db.Column(db.Text,nullable=False)
    rating_by_who=db.Column(db.Text,nullable=False)
    created_at = db.Column(db.String(120), default=(datetime.now().strftime("%d.%m.%Y")))
    updated_at = db.Column(db.String(120), onupdate=(datetime.now().strftime("%d.%m.%Y")))

    def __repr__(self) -> str:
        return 'Rating>>>{self.goal_id}'
