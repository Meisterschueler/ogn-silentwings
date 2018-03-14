import unittest

from datetime import date

from app import create_app, db
from app.silent_wings import create_active_contests_string
from app.model import Contest, Location


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
        self.maxDiff = None     # long test string means long diffs

        # Create simple contest
        contest = Contest()
        contest.name = "My Fake Contest"
        contest.category = None
        contest.country = "FR"
        contest.end_date = date(2005, 9, 12)
        contest.featured = None
        contest.start_date = date(2005, 9, 3)
        contest.time_zone = None

        location = Location()
        location.name = "St. Auban"
        location.country = "FR"
        location.latitude = 44.1959
        location.longitude = 5.98849
        location.altitude = None

        contest.location = location

        # Put the contest into the database
        db.session.add(contest)
        db.session.add(location)
        db.session.commit()

        # Check if the string for silent wings is correct
        message = create_active_contests_string()
        silent_wings_string = ("{contestname}MYFAKECONTEST{/contestname}"
                               "{contestdisplayname}My Fake Contest{/contestdisplayname}"
                               "{datadelay}15{/datadelay}"
                               "{utcoffset}+01:00{/utcoffset}"
                               "{countrycode}FR{/countrycode}"
                               "{site}St. Auban{/site}"
                               "{fromdate}20050903{/fromdate}"
                               "{todate}20050912{/todate}"
                               "{lat}44.1959{/lat}"
                               "{lon}5.98849{/lon}"
                               "{alt}{/alt}")
        self.assertEqual(message, silent_wings_string)


if __name__ == '__main__':
    unittest.main()
