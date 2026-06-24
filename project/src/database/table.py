#!/usr/bin/python3
import sqlalchemy as db
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class WeatherRecord(Base):
    __tablename__ = "weather"
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(255))
    device_id = db.Column("deviceId", db.Integer)
    rainfall = db.Column(db.Integer)
    forecast = db.Column(db.String(255))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    temperature = db.Column(db.Float)
    time = db.Column(db.DateTime)

    # relationships
    weather_children = relationship(
        "GymCapacityRecord", back_populates="weather_parent"
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Coordinate(Base):
    __tablename__ = "coordinate"
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(255), unique=True)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    time = db.Column(db.DateTime)

    # relationships
    coordinate_children = relationship(
        "GymCapacityRecord", back_populates="coordinate_parent"
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class GymCapacityRecord(Base):
    __tablename__ = "gym_capacity"
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer)
    location = db.Column(db.String(255))
    weather_id = db.Column(db.Integer, db.ForeignKey(WeatherRecord.id), unique=True)
    coordinate_id = db.Column(db.Integer, db.ForeignKey(Coordinate.id), unique=True)
    capacity = db.Column(db.Integer, default=0)
    public_holiday = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    # # relationships
    weather_parent = relationship("WeatherRecord", back_populates="weather_children")
    coordinate_parent = relationship("Coordinate", back_populates="coordinate_children")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class DatacampCourse(Base):
    __tablename__ = "datacamp_courses"
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(50), nullable=False, unique=True)
    course_instructor = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(20), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


weather = WeatherRecord
coordinate = Coordinate
gym_capacity = GymCapacityRecord
datacamp_courses = DatacampCourse
