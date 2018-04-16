import unittest
from unittest import mock
from datetime import date

from app import create_app, db
from app.utils import process_beacon, logfile_to_beacons, ddb_import
from app.model import Beacon


class ogn_ddb_response:
    # OGN DDB http://ddb.glidernet.org/download/
    text = "#DEVICE_TYPE,DEVICE_ID,AIRCRAFT_MODEL,REGISTRATION,CN,TRACKED,IDENTIFIED\n'F','000000','HPH 304CZ-17','OK-7777','KN','Y','Y'\n'O','000001','Paraglider','','','Y','Y'\n'F','000002','LS-6 18','OY-XRG','G2','Y','Y'\n'F','00000D','Ka-8','D-1749','W5','Y','Y'\n'F','0000FD','Taurus','F-JRDN','DN','Y','Y'\n'F','000114','','','','N','N'"


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

    def test_import_single_beacon(self):
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

    def test_import_logfile(self):
        import os

        # Get all the beacons
        logfile = 'OGN_log.txt_2018-01-18_3minutes.gz'
        base_path = os.path.dirname(__file__)
        path = os.path.join(base_path, logfile)
        beacons = logfile_to_beacons(path, reference_date=date(2018, 1, 18))

        # Put the beacons from logfile into db
        db.session.add_all(beacons)
        db.session.commit()

        # Check if all 6014 are inserted
        db_beacons = db.session.query(Beacon).all()
        self.assertEqual(len(db_beacons), 6014)

    @mock.patch('app.utils.requests')
    def test_ddb_import(self, requests_mock):
        requests_mock.get.side_effect = [ogn_ddb_response]

        ddb_entries = ddb_import()
        self.assertEqual(len(ddb_entries), 6, "Pass")


if __name__ == '__main__':
    unittest.main()
