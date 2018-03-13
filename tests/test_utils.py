import unittest

from datetime import date

from app import create_app, db
from app.utils import process_beacon
from app.model import Beacon


class TestDB(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test(self):
        # Create beacon from raw aprs message.
        raw_flarm_message = "FLRDF0AAD>APRS,qAS,YBSS:/065751h3743.64S/14425.51E'146/004/A=000492 !W62! id0ADF0AAD -078fpm +2.3rot 10.8dB 0e -7.7kHz gps1x2"
        flarm_message = process_beacon(raw_flarm_message, reference_date=date(2018, 3, 11))
        flarm_beacon = Beacon(**flarm_message)

        # Put the beacon into the db
        db.session.add(flarm_beacon)
        db.session.commit()

        # Get one beacon from db and check if it is the beacon from above
        beacon_query = db.session.query(Beacon)
        beacon = beacon_query.one()
        self.assertEqual(beacon.name, "FLRDF0AAD")


if __name__ == '__main__':
    unittest.main()
