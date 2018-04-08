import unittest

from app import create_app, db
from app.glidertracker import glidertracker_filter, glidertracker_contests

from tests.helper import create_simple_contest, create_simple_tracker_data


class TestDB(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        # Put an example contest with tracker data into the database
        contest = create_simple_contest()
        beacons = create_simple_tracker_data()
        db.session.add(contest)
        db.session.add_all(beacons)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_glidertracker_filter(self):
        self.maxDiff = None

        # In the open class we have two contestants
        message = glidertracker_filter("MYFAKECONTEST_OPEN")
        glidertracker_filter_string = ('ID,CALL,CN,TYPE\n'
                                       '"FLRDD0815","D-KONI","KG","Eta"\n'
                                       '"FLRDD4711","D-1900","XX","Nimeta"')
        self.assertMultiLineEqual(message, glidertracker_filter_string)

        # In the club class we have only one contestant
        message = glidertracker_filter("MYFAKECONTEST_18METER")
        glidertracker_filter_string = ('ID,CALL,CN,TYPE\n'
                                       '"OGN0123","D-KUGL","GL","ASG 29"')
        self.assertMultiLineEqual(message, glidertracker_filter_string)

    def test_glidertracker_contests(self):
        message = glidertracker_contests()
        glidertracker_contests_string = ("MYFAKECONTEST_OPEN\n"
                                         "MYFAKECONTEST_18METER")
        self.assertMultiLineEqual(message, glidertracker_contests_string)


if __name__ == '__main__':
    unittest.main()
