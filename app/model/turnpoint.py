from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from app import db


class Turnpoint(db.Model):
    __tablename__ = "turnpoints"
    # <Turnpoint 1: Aarberg Bf,0.82107561826706,0.12703087925911,449,3,finish,False,161607.8125,5.3836393356323,0.0,previous,5000,0,180.0000000000004,128.45981235234487,0.0,False,0,False,False,finish>

    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Integer)
    point_index = Column(Integer)   # number within task
    type = Column(String)           # start/point/finish
    multiple_start = Column(Boolean) # Flag to allow multiple starts
    distance = Column(Float)        # Distance to turnpoint
    course_in = Column(Float)       # Course to turnpoint
    course_out = Column(Float)      # Course to next turnpoint
    oz_type = Column(String)        # next/symmetric/previous/fixed/start 
    oz_radius1 = Column(Integer)    # First radius (must be greater than second radius) / 10km for DAEC Keyhole / unit is meters
    oz_radius2 = Column(Integer)    # Second radius / 0,5 for DAEC Keyhole / unit is meters
    oz_angle1 = Column(Float)       # Angle of first radius / 45 for DAEC Keyhole / unit is degrees
    oz_angle12 = Column(Float)      # if oz_type = fixed then this value orients the observation zone - disregard otherwise
    oz_angle2 = Column(Float)       # Angel of second radius / 180 for DAEC Keyhole
    oz_line = Column(Boolean)       # True of observation zone is line
    oz_max_altitude = Column(Integer)   # maximum Altitute of Turnpoint
    oz_move = Column(Boolean)       # Moves origin of task leg intersection with observation zone to minimum - disregard - False
    oz_reduce = Column(Boolean)     # Reduces leg distance - disregard
    speed_section_type = Column(String) # Start/finish/point 

    # Relations
    task_id = Column(Integer, ForeignKey('tasks.id', ondelete='SET NULL'))
    task = relationship('Task', foreign_keys=[task_id], backref=backref('turnpoints', order_by='Turnpoint.point_index.asc()'))

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
