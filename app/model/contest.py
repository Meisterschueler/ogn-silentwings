from sqlalchemy import Column, String, Integer, Date, Boolean
from app import db


class Contest(db.Model):
    __tablename__ = "contests"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String)
    country = Column(String)
    end_date = Column(Date)
    featured = Column(Boolean)
    start_date = Column(Date)
    time_zone = Column(String)

    def __repr__(self):
        return "<Contest %s: %s,%s,%s,%s,%s,%s,%s>" % (
            self.id,
            self.name,
            self.category,
            self.country,
            self.end_date,
            self.featured,
            self.start_date,
            self.time_zone)
