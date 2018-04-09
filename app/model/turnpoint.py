from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app import db


class Turnpoint(db.Model):
    __tablename__ = "turnpoints"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Integer)
    point_index = Column(Integer)   # number within task
    type = Column(String)           # start/point/finish
    multiple_start = Column(Boolean)
    distance = Column(Float)
    course_in = Column(Float)
    course_out = Column(Float)
    oz_type = Column(String)        # next/symmetric/previous
    oz_radius1 = Column(Integer)
    oz_radius2 = Column(Integer)
    oz_angle1 = Column(Float)
    oz_angle12 = Column(Float)
    oz_angle2 = Column(Float)
    oz_line = Column(Boolean)
    oz_max_altitude = Column(Integer)
    oz_move = Column(Boolean)
    oz_reduce = Column(Boolean)
    speed_section_type = Column(String)

    # Relations
    task_id = Column(Integer, ForeignKey('tasks.id', ondelete='SET NULL'))
    task = relationship('Task', foreign_keys=[task_id], backref='turnpoints')

    def __repr__(self):
        return "<Turnpoint %s: %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s>" % (
            self.id,
            self.name,
            self.latitude,
            self.longitude,
            self.elevation,
            self.point_index,
            self.type,
            self.multiple_start,
            self.distance,
            self.course_in,
            self.course_out,
            self.oz_type,
            self.oz_radius1,
            self.oz_radius2,
            self.oz_angle1,
            self.oz_angle12,
            self.oz_angle2,
            self.oz_line,
            self.oz_max_altitude,
            self.oz_move,
            self.oz_reduce,
            self.speed_section_type)
