import unittest

from datetime import date

from app import create_app, db
from app.silent_wings import get_active_contests
from app.model import Contest


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
        contest.name = 'My Fake Contest'
        contest.category = None
        contest.country = "FR"
        contest.end_date = date(2005, 9, 12)
        contest.featured = None
        contest.start_date = date(2005, 9, 3)
        contest.time_zone = "+01:00"

        # Put the contest into the database
        db.session.add(contest)
        db.session.commit()

        # Check if the string for silent wings is correct
        message = get_active_contests()
        self.assertEqual(message, "{contestname}MYFAKECONTEST{/contestname}{contestdisplayname}My Fake Contest{/contestdisplayname}{datadelay}15{/datadelay}{utcoffset}+01:00{/utcoffset}{countrycode}FR{/countrycode}{site}St. Auban{/site}{fromdate}20050903{/fromdate}{todate}20050912{/todate}{lat}44.1959{/lat}{lon}5.98849{/lon}{alt}{/alt}")


if __name__ == '__main__':
    unittest.main()
