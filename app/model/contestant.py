from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app import db


class Contestant(db.Model):
    __tablename__ = "contestants"

    id = Column(Integer, primary_key=True)
    aircraft_model = Column(String)
    aircraft_registration = Column(String)
    club = Column(String)
    contestant_number = Column(String)
    handicap = Column(String)
    name = Column(String)
    not_competing = Column(Boolean)
    pure_glider = Column(Boolean)
    sponsors = Column(String)

    # Relations
    contest_class_id = Column(Integer, ForeignKey('contest_classes.id', ondelete='SET NULL'))
    contest_class = relationship('ContestClass', foreign_keys=[contest_class_id], backref='contestants')

    def __repr__(self):
        return "<Contestant %s: %s,%s,%s,%s,%s,%s,%s,%s,%s>" % (
            self.id,
            self.aircraft_model,
            self.aircraft_registration,
            self.club,
            self.contestant_number,
            self.handicap,
            self.name,
            self.not_competing,
            self.pure_glider,
            self.sponsors)
