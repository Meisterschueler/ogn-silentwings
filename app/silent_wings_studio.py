from app.model import Contest, Task
from app import db

import json
import time


def create_eventgroups_json():
    competitions = list()
    for contest in db.session.query(Contest):
        for contest_class in contest.classes:
            competition_dict = dict()
            competition_dict['name'] = '{0} - {1}'.format(contest.name, contest_class.category)
            competition_dict['description'] = 'Contest: {0}, category: {1}'.format(contest.name, contest_class.type)
            competition_dict['bannerUrl'] = 'No banner url'
            competition_dict['events'] = list()
            for task in contest_class.tasks:
                event = dict()
                event['id'] = task.id
                event['startOpenTs'] = time.mktime(task.no_start.timetuple())
                competition_dict['events'].append(event)

            competitions.append(competition_dict)

    return json.dumps(competitions, indent=4)


def create_event_json(task_id):
    task_query = db.session.query(Task) \
        .filter(Task.id == task_id)

    task = task_query.one()
    event = dict()
    event['name'] = task.contest_class.contest.name
    event['description'] = 'Contest: {0}, category: {1}, day: {2}'.format(task.contest_class.contest.name,
                                                                          task.contest_class.type,
                                                                          task.task_date)
    event['revision'] = 0
    event['task'] = dict()
    event['task']['taskName'] = 'Name of da task'
    event['task']['taskType'] = task.task_type
    event['task']['startOpenTs'] = time.mktime(task.no_start.timetuple())

    return json.dumps(event, indent=4)
