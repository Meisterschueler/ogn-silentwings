from datetime import date, datetime

from app.model import Contest, Location, ContestClass, Task, Contestant, Pilot,\
    Beacon


def print_contest(contest):
    print(contest)
    print(contest.location)
    for contest_class in contest.classes:
        print(contest_class)
        for task in contest_class.tasks:
            print(task)
            for turnpoint in task.turnpoints:
                print(turnpoint)
        for contestant in contest_class.contestants:
            print(contestant)
            for pilot in contestant.pilots:
                print(pilot)


def create_simple_contest():
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
    open_class.category = "glider"
    open_class.type = "Open"
    open_class.contest = contest

    m18_class = ContestClass()
    m18_class.category = "glider"
    m18_class.type = "18-meter"
    m18_class.contest = contest

    contestant_open_1 = Contestant()
    contestant_open_1.aircraft_model = "Eta"
    contestant_open_1.aircraft_registration = "D-KONI"
    contestant_open_1.contestant_number = "KG"
    contestant_open_1.live_track_id = "FLRDD0815"
    contestant_open_1.contest_class = open_class

    pilot_open_1 = Pilot()
    pilot_open_1.first_name = "Konstantin"
    pilot_open_1.last_name = "Gründger"
    pilot_open_1.contestant = contestant_open_1

    contestant_open_2 = Contestant()
    contestant_open_2.aircraft_model = "Nimeta"
    contestant_open_2.aircraft_registration = "D-1900"
    contestant_open_2.contestant_number = "XX"
    contestant_open_2.live_track_id = "FLRDD4711"
    contestant_open_2.contest_class = open_class

    pilot_open_2 = Pilot()
    pilot_open_2.first_name = "Dagobert"
    pilot_open_2.last_name = "Duck"
    pilot_open_2.contestant = contestant_open_2

    contestant_18m_1 = Contestant()
    contestant_18m_1.aircraft_model = "ASG 29"
    contestant_18m_1.aircraft_registration = "D-KUGL"
    contestant_18m_1.contestant_number = "GL"
    contestant_18m_1.live_track_id = "OGN0123"
    contestant_18m_1.contest_class = m18_class

    pilot_18m_1 = Pilot()
    pilot_18m_1.first_name = "Gundel"
    pilot_18m_1.last_name = "Gaukelei"
    pilot_18m_1.contestant = contestant_18m_1

    task_1 = Task()
    task_1.no_start = datetime(2015, 9, 3, 10, 0, 0)
    task_1.task_type = "High speed"
    task_1.task_date = date(2005, 9, 3)
    task_1.contest_class = open_class

    task_2 = Task()
    task_2.no_start = datetime(2015, 9, 4, 10, 0, 0)
    task_2.task_date = date(2005, 9, 4)
    task_2.contest_class = open_class

    task_3 = Task()
    task_3.no_start = datetime(2015, 9, 7, 10, 0, 0)
    task_3.task_date = date(2005, 9, 7)
    task_3.contest_class = open_class

    return contest


def create_simple_tracker_data():
    beacons = list()
    beacons.append(Beacon(**{'address': "FLRDD0815", 'timestamp': datetime(2015, 9, 3, 10, 1, 23), 'latitude': 44.203, 'longitude': 5.95, 'altitude': 1009}))
    beacons.append(Beacon(**{'address': "FLRDD0815", 'timestamp': datetime(2015, 9, 3, 10, 1, 24), 'latitude': 44.204, 'longitude': 5.94, 'altitude': 1011}))
    beacons.append(Beacon(**{'address': "FLRDD0815", 'timestamp': datetime(2015, 9, 3, 10, 1, 25), 'latitude': 44.205, 'longitude': 5.93, 'altitude': 1013}))
    beacons.append(Beacon(**{'address': "FLRDD4711", 'timestamp': datetime(2015, 9, 3, 10, 1, 22), 'latitude': 44.2, 'longitude': 5.9, 'altitude': 1000}))

    return beacons
