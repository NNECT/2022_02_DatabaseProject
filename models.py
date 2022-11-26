import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

templatesDir = os.path.abspath(os.getcwd()) + "\\templates"
staticDir = os.path.abspath(os.getcwd()) + "\\static"

app = Flask(__name__, template_folder=templatesDir, static_folder=staticDir)

app.config['SECRET_KEY'] = 'this is secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.getcwd()) + "\\db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)
db.app = app


class Location(db.Model):
    __tablename__ = 'location'
    location_id = db.Column(db.Integer, primary_key=True, nullable=False)
    location_name = db.Column(db.String(10), nullable=False)


class ClimateYear(db.Model):
    __tablename__ = 'climate_year'
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), primary_key=True, nullable=False)
    chk_date = db.Column(db.String(4), primary_key=True, nullable=False)
    tavg = db.Column(db.Float)
    tmin = db.Column(db.Float)
    tmax = db.Column(db.Float)
    rain_total = db.Column(db.Float)
    rain_max = db.Column(db.Float)
    humid_avg = db.Column(db.Float)
    wind_avg = db.Column(db.Float)
    light_time = db.Column(db.Float)


class ClimateMonte(db.Model):
    __tablename__ = 'climate_month'
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), primary_key=True, nullable=False)
    chk_date = db.Column(db.String(7), primary_key=True, nullable=False)
    tavg = db.Column(db.Float)
    tmin = db.Column(db.Float)
    tmax = db.Column(db.Float)
    rain_total = db.Column(db.Float)
    rain_max = db.Column(db.Float)
    humid_avg = db.Column(db.Float)
    wind_avg = db.Column(db.Float)
    wind_max = db.Column(db.Float)
    light_time = db.Column(db.Float)


class ClimateDay(db.Model):
    __tablename__ = 'climate_day'
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'), primary_key=True, nullable=False)
    chk_date = db.Column(db.String(10), primary_key=True, nullable=False)
    tavg = db.Column(db.Float)
    tmin = db.Column(db.Float)
    tmax = db.Column(db.Float)
    rain = db.Column(db.Float)
    humid_avg = db.Column(db.Float)
    wind_avg = db.Column(db.Float)
    wind_max = db.Column(db.Float)
    light_time = db.Column(db.Float)