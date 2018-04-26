from sqlalchemy import Column, String, Integer, Float, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app import db


class Task(db.Model):
    __tablename__ = "tasks"
    # example: <Task 1: 2018-04-19 00:00:01,preliminary,False,2018-04-19,1737118.5,0.0,0.0,2,2,unknown_triangle,-1>

    id = Column(Integer, primary_key=True)
    images = None   # Column(Integer)
    no_start = Column(DateTime)     # e.g. 2018-04-19 00:00:01
    result_status = Column(String)  # e.g. preliminary
    start_on_entry = Column(Boolean)    # e.g. false
    task_date = Column(Date)        # e.g. 2018-04-19
    task_distance = Column(Float)   # provided in meters e.g. 1737118.5
    task_distance_max = Column(Float)   # is zero if racing task? TBC.
    task_distance_min = Column(Float)   # is zero if racing task? TBC.
    task_duration = Column(Integer)  # in seconds
    task_number = Column(Integer)
    task_type = Column(String)      # e.g. unknown_triangle
    task_value = Column(Integer)    # e.g. -1 meaning unclear

    # Relations
    contest_class_id = Column(Integer, ForeignKey('contest_classes.id', ondelete='SET NULL'))
    contest_class = relationship('ContestClass', foreign_keys=[contest_class_id], backref='tasks')

    def __repr__(self):
        return "<Task %s: %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s>" % (
            self.id,
            self.no_start,
            self.result_status,
            self.start_on_entry,
            self.task_date,
            self.task_distance,
            self.task_distance_max,
            self.task_distance_min,
            self.task_duration,
            self.task_number,
            self.task_type,
            self.task_value)
