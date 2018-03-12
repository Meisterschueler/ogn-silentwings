from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app import db


class Pilot(db.Model):
    __tablename__ = "pilots"

    id = Column(Integer, primary_key=True)
    civl_id = Column(Integer)
    email = Column(String)
    first_name = Column(String)
    igc_id = Column(Integer)
    last_name = Column(String)
    nationality = Column(String)

    # Relations
    contestant_id = Column(Integer, ForeignKey('contestants.id', ondelete='SET NULL'))
    contestant = relationship('Contestant', foreign_keys=[contestant_id], backref='pilots')

    def __repr__(self):
        return "<Pilot %s: %s,%s,%s,%s,%s,%s>" % (
            self.id,
            self.civl_id,
            self.email,
            self.first_name,
            self.igc_id,
            self.last_name,
            self.nationality)
