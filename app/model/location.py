from sqlalchemy import Column, String, Integer, Float
from app import db


class Location(db.Model):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Integer)
    time_zone = Column(String)

    def __repr__(self):
        return "<Location %s: %s,%s,%s,%s,%s,%s>" % (
            self.id,
            self.name,
            self.country,
            self.latitude,
            self.longitude,
            self.altitude,
            self.time_zone)
