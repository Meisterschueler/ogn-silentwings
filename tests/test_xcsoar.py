import unittest

from app import create_app, db
from app.model import Task
from app.xcsoar import write_xcsoar_task
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

    def test_xcsoar_export(self):
        import io
        fp = io.BytesIO()
        task = db.session.query(Task).first()
        write_xcsoar_task(fp, task)
        xml = fp.getvalue()
        
        print(xml)

if __name__ == '__main__':
    unittest.main()
