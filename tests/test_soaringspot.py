import unittest
from unittest import mock

from app import create_app, db
from app.soaringspot import get_soaringspot_document, get_soaringspot_contests


class root_document:
    text = '{"_links":{"self":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/"},"http:\\/\\/api.soaringspot.com\\/rel\\/contests":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/contests"},"http:\\/\\/api.soaringspot.com\\/rel\\/tasks":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/tasks"}},"_embedded":{"http:\\/\\/api.soaringspot.com\\/rel\\/contests":[{"id":1891,"name":"SoaringSpot 3D Tracking Interface","start_date":"2018-03-03","end_date":"2018-03-16","featured":false,"time_zone":"Asia\\/Kabul","country":"AF","category":"glider","_links":{"self":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/contests\\/1891"},"http:\\/\\/api.soaringspot.com\\/rel\\/classes":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/contests\\/1891\\/classes"},"http:\\/\\/api.soaringspot.com\\/rel\\/location":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/locations\\/23221"},"http:\\/\\/api.soaringspot.com\\/rel\\/winners":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/contests\\/1891\\/winners"},"http:\\/\\/api.soaringspot.com\\/rel\\/downloads":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/contests\\/1891\\/downloads"},"http:\\/\\/api.soaringspot.com\\/rel\\/upload\\/flight":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/contests\\/1891\\/flights"},"http:\\/\\/api.soaringspot.com\\/rel\\/www":{"href":"http:\\/\\/www.test.soaringspot.com\\/en_gb\\/soaringspot-3d-tracking-interface-pain-guzar-2018\\/"}},"_embedded":{"http:\\/\\/api.soaringspot.com\\/rel\\/classes":[{"id":3471,"category":"glider","type":"open","_links":{"self":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/classes\\/3471"},"http:\\/\\/api.soaringspot.com\\/rel\\/contest":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/contests\\/1891"},"http:\\/\\/api.soaringspot.com\\/rel\\/contestants":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/classes\\/3471\\/contestants"},"http:\\/\\/api.soaringspot.com\\/rel\\/tasks":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/classes\\/3471\\/tasks"},"http:\\/\\/api.soaringspot.com\\/rel\\/class_results":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/classes\\/3471\\/results"}}},{"id":3470,"category":"glider","type":"18_meter","_links":{"self":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/classes\\/3470"},"http:\\/\\/api.soaringspot.com\\/rel\\/contest":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/contests\\/1891"},"http:\\/\\/api.soaringspot.com\\/rel\\/contestants":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/classes\\/3470\\/contestants"},"http:\\/\\/api.soaringspot.com\\/rel\\/tasks":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/classes\\/3470\\/tasks"},"http:\\/\\/api.soaringspot.com\\/rel\\/class_results":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/classes\\/3470\\/results"}}}],"http:\\/\\/api.soaringspot.com\\/rel\\/location":{"name":"P\\u0101\\u2019\\u012bn Guz\\u0304ar","time_zone":"Asia\\/Kabul","country":"AF","altitude":937,"latitude":0.6235190498079,"longitude":1.1184172821206,"_links":{"self":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/locations\\/23221"}}}}}]}}'


class contestant_document:
    text = '{"_links":{"self":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/classes\\/3471\\/contestants"}},"_embedded":{"http:\\/\\/api.soaringspot.com\\/rel\\/contestants":[{"name":"TestVorname TestNachmae","club":"TestClub","aircraft_model":"asw 22\\/22m","contestant_number":"IX","aircraft_registration":"K-KNIX","pure_glider":true,"not_competing":false,"handicap":119,"live_track_id":"FLRDDXXXX","sponsors":"none","_links":{"self":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/contestants\\/3639607298"}},"_embedded":{"http:\\/\\/api.soaringspot.com\\/rel\\/pilot":[{"first_name":"TestVorname","last_name":"TestNachmae","email":"loechen@gmx.de","nationality":"DE","civl_id":0,"igc_id":0}]}},{"name":"VornameTest NachnameTest","aircraft_model":"ask 13","contestant_number":"99","aircraft_registration":"D-0099","pure_glider":true,"flight_recorders":"FlightRecorderTest\\r\\n","not_competing":false,"handicap":79,"live_track_id":"FLRDDXXXX","_links":{"self":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/contestants\\/3639607297"}},"_embedded":{"http:\\/\\/api.soaringspot.com\\/rel\\/pilot":[{"first_name":"VornameTest","last_name":"NachnameTest","email":"bla@blub.de","nationality":"DE","civl_id":0,"igc_id":0}]}}]}}'


class task_document:
    text = '{"_links":{"self":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/classes\\/3471\\/tasks"}},"_embedded":{"http:\\/\\/api.soaringspot.com\\/rel\\/tasks":[{"task_date":"2018-03-03","task_number":3,"result_status":"preliminary","task_type":"unknown_triangle","task_value":-1,"task_distance":101576.90625,"task_distance_min":0,"task_distance_max":0,"task_duration":0,"no_start":"2018-03-03T00:00:00","start_on_entry":false,"_links":{"self":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/tasks\\/3639607299"},"http:\\/\\/api.soaringspot.com\\/rel\\/task\\/download":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/tasks\\/3639607299\\/download"},"http:\\/\\/api.soaringspot.com\\/rel\\/points":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/tasks\\/3639607299\\/points"},"http:\\/\\/api.soaringspot.com\\/rel\\/results":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/tasks\\/3639607299\\/results"},"http:\\/\\/api.soaringspot.com\\/rel\\/images":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/tasks\\/3639607299\\/images"},"http:\\/\\/api.soaringspot.com\\/rel\\/class":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/classes\\/3471"}},"_embedded":{"http:\\/\\/api.soaringspot.com\\/rel\\/images":[]}},{"task_date":"2018-03-03","task_number":2,"result_status":"preliminary","task_type":"unknown","task_value":-1,"task_distance":0,"task_distance_min":0,"task_distance_max":0,"task_duration":0,"no_start":"2018-03-03T00:00:00","start_on_entry":false,"_links":{"self":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/tasks\\/3639607298"},"http:\\/\\/api.soaringspot.com\\/rel\\/task\\/download":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/tasks\\/3639607298\\/download"},"http:\\/\\/api.soaringspot.com\\/rel\\/points":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/tasks\\/3639607298\\/points"},"http:\\/\\/api.soaringspot.com\\/rel\\/results":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/tasks\\/3639607298\\/results"},"http:\\/\\/api.soaringspot.com\\/rel\\/images":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/tasks\\/3639607298\\/images"},"http:\\/\\/api.soaringspot.com\\/rel\\/class":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/classes\\/3471"}},"_embedded":{"http:\\/\\/api.soaringspot.com\\/rel\\/images":[]}},{"task_date":"2018-03-03","task_number":1,"result_status":"preliminary","task_type":"unknown","task_value":-1,"task_distance":0,"task_distance_min":0,"task_distance_max":0,"task_duration":0,"no_start":"2018-03-03T00:00:00","start_on_entry":false,"_links":{"self":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/tasks\\/3639607297"},"http:\\/\\/api.soaringspot.com\\/rel\\/task\\/download":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/tasks\\/3639607297\\/download"},"http:\\/\\/api.soaringspot.com\\/rel\\/points":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/tasks\\/3639607297\\/points"},"http:\\/\\/api.soaringspot.com\\/rel\\/results":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/tasks\\/3639607297\\/results"},"http:\\/\\/api.soaringspot.com\\/rel\\/images":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/tasks\\/3639607297\\/images"},"http:\\/\\/api.soaringspot.com\\/rel\\/class":{"href":"http:\\/\\/api.test.soaringspot.com\\/v1\\/classes\\/3471"}},"_embedded":{"http:\\/\\/api.soaringspot.com\\/rel\\/images":[]}}]}}'


class no_task_document:
    text = '{"code":404,"message":"Class with 3470 id does not have any tasks."}'


def print_all_contests(contests):
    for contest in contests:
            print(contest)
            print(contest.location)
            for contest_class in contest.classes:
                print(contest_class)
                for task in contest_class.tasks:
                    print(task)
                for contestant in contest_class.contestants:
                    print(contestant)
                    for pilot in contestant.pilots:
                        print(pilot)


class TestDB(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.base_url = self.app.config['SOARINGSPOT_BASE_URL']
        self.client_id = self.app.config['SOARINGSPOT_CLIENT_ID']
        self.secret = self.app.config['SOARINGSPOT_SECRET']

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @mock.patch('app.soaringspot.requests')
    def test_local_document(self, requests_mock):
        requests_mock.get.side_effect = [root_document,
                                         contestant_document, task_document,
                                         contestant_document, no_task_document]

        document = get_soaringspot_document(url=self.base_url, client_id=self.client_id, secret=self.secret)
        print(document)

    @mock.patch('app.soaringspot.requests')
    def test_local_objects(self, requests_mock):
        requests_mock.get.side_effect = [root_document,
                                         contestant_document, task_document,
                                         contestant_document, no_task_document]

        contests = get_soaringspot_contests(url=self.base_url, client_id=self.client_id, secret=self.secret)
        print_all_contests(contests)

        db.session.add_all(contests)
        db.session.commit()

    def test_remote_document(self):
        document = get_soaringspot_document(url=self.base_url, client_id=self.client_id, secret=self.secret)
        print(document)

    def test_remote_objects(self):
        contests = get_soaringspot_contests(url=self.base_url, client_id=self.client_id, secret=self.secret)
        print_all_contests(contests)

        db.session.add_all(contests)
        db.session.commit()


if __name__ == '__main__':
    unittest.main()
