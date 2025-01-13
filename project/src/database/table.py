from sqlalchemy.orm import declarative_base, relationship
import sqlalchemy as db

Base = declarative_base()

class weather(Base):
    __tablename__   = 'weather'
    id              = db.Column(db.Integer, primary_key=True )
    area            = db.Column(db.String(255))
    deviceId        = db.Column(db.Integer)
    rainfall        = db.Column(db.Integer)
    forecast        = db.Column(db.String(255))
    temperature     = db.Column(db.Float)
    time            = db.Column(db.DateTime)

    # relationships
    children      = relationship("gym_capacity", back_populates="parent")
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class gym_capacity(Base):
    __tablename__   = 'gym_capacity'
    id              = db.Column(db.Integer, primary_key=True)
    unit_id         = db.Column(db.Integer)
    location        = db.Column(db.String(255))
    weather_id      = db.Column(db.Integer, db.ForeignKey(weather.id), unique=True)
    capacity        = db.Column(db.Integer, default=0)
    public_holiday  = db.Column(db.Boolean, default=False)
    created_at      = db.Column(db.DateTime)
    updated_at      = db.Column(db.DateTime)
    # # relationships
    parent       = relationship("weather", back_populates="children")
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class datacamp_courses(Base):
    __tablename__       = 'datacamp_courses'
    id           = db.Column(db.Integer, primary_key=True)
    course_name         = db.Column(db.String(50),nullable=False, unique=True)
    course_instructor   = db.Column(db.String(100),nullable=False)
    topic               = db.Column(db.String(20),nullable=False)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}