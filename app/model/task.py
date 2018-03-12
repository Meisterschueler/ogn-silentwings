from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app import db


class Task(db.Model):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    images = None   # Column(Integer)
    no_start = Column(DateTime)
    result_status = Column(String)
    start_on_entry = Column(Boolean)
    task_date = Column(String)
    task_distance = Column(Float)
    task_distance_max = Column(Float)
    task_distance_min = Column(Float)
    task_duration = Column(String)
    task_number = Column(Integer)
    task_type = Column(String)
    task_value = Column(Integer)

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
