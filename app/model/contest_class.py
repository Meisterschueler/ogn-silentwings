from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app import db


class ContestClass(db.Model):
    __tablename__ = "contest_classes"

    id = Column(Integer, primary_key=True)
    category = Column(String)
    type = Column(String)

    # Relations
    contest_id = Column(Integer, ForeignKey('contests.id', ondelete='SET NULL'))
    contest = relationship('Contest', foreign_keys=[contest_id], backref='classes')

    def __repr__(self):
        return "<ContestClass %s: %s,%s>" % (
            self.id,
            self.category,
            self.type)
