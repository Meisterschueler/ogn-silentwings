from sqlalchemy import Column, String, Integer, Float, DateTime
from app import db


class Beacon(db.Model):
    __tablename__ = "beacons"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    timestamp = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)
    track = Column(Float)
    ground_speed = Column(Float)
    climb_rate = Column(Float)
    turn_rate = Column(Float)

    def __repr__(self):
        return "<Beacon %s: %s,%s,%s,%s,%s,%s,%s,%s,%s,%s>" % (
            self.id,
            self.name,
            self.address,
            self.timestamp,
            self.latitude,
            self.longitude,
            self.altitude,
            self.track,
            self.ground_speed,
            self.climb_rate,
            self.turn_rate)
