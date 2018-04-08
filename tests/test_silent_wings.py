import unittest

from app import create_app, db
from app.silent_wings import create_active_contests_string, create_contest_info_string,\
    create_cuc_pilots_block, create_tracker_data
from app.silent_wings_studio import create_eventgroups_json, create_event_json

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

    def test_silent_wings_viewer(self):
        self.maxDiff = None     # long test_silent_wings_viewer string means long diffs

        # Check if the strings for silent wings are correct
        # Check answer to getactivecontests.php
        message = create_active_contests_string()
        silent_wings_string = ("{contestname}MYFAKECONTEST_OPEN{/contestname}"
                               "{contestdisplayname}My Fake Contest Open{/contestdisplayname}"
                               "{datadelay}15{/datadelay}"
                               "{utcoffset}+01:00{/utcoffset}"
                               "{countrycode}FR{/countrycode}"
                               "{site}St. Auban{/site}"
                               "{fromdate}20050903{/fromdate}"
                               "{todate}20050912{/todate}"
                               "{lat}44.1959{/lat}"
                               "{lon}5.98849{/lon}"
                               "{alt}{/alt}\n"

                               "{contestname}MYFAKECONTEST_18METER{/contestname}"
                               "{contestdisplayname}My Fake Contest 18-meter{/contestdisplayname}"
                               "{datadelay}15{/datadelay}"
                               "{utcoffset}+01:00{/utcoffset}"
                               "{countrycode}FR{/countrycode}"
                               "{site}St. Auban{/site}"
                               "{fromdate}20050903{/fromdate}"
                               "{todate}20050912{/todate}"
                               "{lat}44.1959{/lat}"
                               "{lon}5.98849{/lon}"
                               "{alt}{/alt}\n"
                               )
        self.assertMultiLineEqual(message, silent_wings_string)

        # Check answer to getcontestinfo
        message = create_contest_info_string("MYFAKECONTEST_OPEN")
        silent_wings_string = (
            "{date}20050903{/date}{task}1{/task}{validday}1{/validday}"
            "{date}20050904{/date}{task}1{/task}{validday}1{/validday}"
            "{date}20050907{/date}{task}1{/task}{validday}1{/validday}")
        self.assertEqual(message, silent_wings_string)

    def test_silent_wings_viewer_tracker_data(self):
        message = create_tracker_data('FLRDD0815')
        silent_wings_string = (
            "{datadelay}6{/datadelay}\n"
            "FLRDD0815,1441274483,44.203,5.95,1009,1\n"
            "FLRDD0815,1441274484,44.204,5.94,1011,1\n"
            "FLRDD0815,1441274485,44.205,5.93,1013,1")
        self.assertEqual(message, silent_wings_string)

    def test_cuc_pilots_block(self):
        message = create_cuc_pilots_block()
        cuc_pilots_block = ('[Pilots]\n'
                            '"Konstantin","Gründger",*0,"FLRDD0815","Eta","D-KONI","KG","",0,"",0,"",1,"",""\n'
                            '"Dagobert","Duck",*0,"FLRDD4711","Nimeta","D-1900","XX","",0,"",0,"",1,"",""\n'
                            '\n'
                            '[Starts]\n')
        self.assertMultiLineEqual(message, cuc_pilots_block)

    def test_silent_wings_studio(self):
        message = create_eventgroups_json()
        print(message)

        import json
        message_json = json.loads(message)
        contest_id = message_json[0]['events'][0]['id']
        message = create_event_json(contest_id)
        print(message)


if __name__ == '__main__':
    unittest.main()
