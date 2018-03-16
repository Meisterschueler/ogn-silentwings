import unittest

from datetime import date

from app import create_app, db
from app.silent_wings import create_active_contests_string, create_contest_info_string,\
    create_cuc_pilots_block
from app.model import Contest, Location, ContestClass, Task, Contestant, Pilot


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

        open_class = ContestClass()
        open_class.category = "OPEN"
        open_class.contest = contest

        contestant_1 = Contestant()
        contestant_1.aircraft_model = "ASG 29"
        contestant_1.aircraft_registration = "D-KONI"
        contestant_1.contestant_number = "KG"
        contestant_1.live_track_id = "FLRDD0815"
        contestant_1.contest_class = open_class

        pilot_1 = Pilot()
        pilot_1.first_name = "Konstantin"
        pilot_1.last_name = "Gründger"
        pilot_1.contestant = contestant_1

        contestant_2 = Contestant()
        contestant_2.aircraft_model = "ASK 13"
        contestant_2.aircraft_registration = "D-1900"
        contestant_2.contestant_number = "XX"
        contestant_2.live_track_id = "FLRDD4711"
        contestant_2.contest_class = open_class

        pilot_2 = Pilot()
        pilot_2.first_name = "Dagobert"
        pilot_2.last_name = "Duck"
        pilot_2.contestant = contestant_2

        task_1 = Task()
        task_1.task_date = date(2005, 9, 3)
        task_1.contest_class = open_class

        task_2 = Task()
        task_2.task_date = date(2005, 9, 4)
        task_2.contest_class = open_class

        task_3 = Task()
        task_3.task_date = date(2005, 9, 7)
        task_3.contest_class = open_class

        # Put the contest into the database
        db.session.add(contest)
        db.session.commit()

        # Check if the strings for silent wings are correct
        # Check answer to getactivecontests.php
        message = create_active_contests_string()
        silent_wings_string = ("{contestname}MYFAKECONTEST_OPEN{/contestname}"
                               "{contestdisplayname}My Fake Contest OPEN{/contestdisplayname}"
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

        # Check answer to getcontestinfo
        message = create_contest_info_string("MYFAKECONTEST_OPEN")
        silent_wings_string = (
            "{date}20050903{/date}{task}1{/task}{validday}0{/validday}"
            "{date}20050904{/date}{task}1{/task}{validday}0{/validday}"
            "{date}20050907{/date}{task}1{/task}{validday}0{/validday}")
        self.assertEqual(message, silent_wings_string)

        message = create_cuc_pilots_block()
        cuc_pilots_block = ('[Pilots]\n'
                            '"Konstantin","Gründger",123,"FLRDD0815","ASG 29","D-KONI","KG","",0,"",0,"",1,"",""\n'
                            '"Dagobert","Duck",123,"FLRDD4711","ASK 13","D-1900","XX","",0,"",0,"",1,"",""')
        self.assertEqual(message, cuc_pilots_block)


if __name__ == '__main__':
    unittest.main()
