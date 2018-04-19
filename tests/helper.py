from datetime import date, datetime

from app.model import Contest, Location, ContestClass, Task, Contestant, Pilot,\
    Beacon, Turnpoint


def print_contest(contest):
    print(contest)
    print(contest.location)
    for contest_class in contest.classes:
        print(contest_class)
        for task in contest_class.tasks:
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

    turnpoint_11 = Turnpoint()
    turnpoint_11.name = "Burgfeuerstein"
    turnpoint_11.type = "start"
    turnpoint_11.oz_radius1 = 3000
    turnpoint_11.point_index = 0
    turnpoint_11.task = task_1

    turnpoint_12 = Turnpoint()
    turnpoint_12.name = "Bayreuth"
    turnpoint_12.type = "point"
    turnpoint_12.oz_radius1 = 3000
    turnpoint_12.point_index = 1
    turnpoint_12.task = task_1

    turnpoint_13 = Turnpoint()
    turnpoint_13.name = "Dobenreuth Hall"
    turnpoint_13.type = "point"
    turnpoint_13.oz_radius1 = 3000
    turnpoint_13.point_index = 2
    turnpoint_13.task = task_1

    turnpoint_14 = Turnpoint()
    turnpoint_14.name = "Burgfeuerstein"
    turnpoint_14.type = "finish"
    turnpoint_14.oz_radius1 = 3000
    turnpoint_14.point_index = 3
    turnpoint_14.task = task_1

    # <Turnpoint None: Burghfeuerstein,0.86904799938202,0.19420191645622,493,3,finish,False,42703.80859375,4.1906170845032,0,previous,3000,0,0.78539816339745,1.0490244309134,0,False,0,False,False,point>
    # <Turnpoint None: Bayreuth,0.87240779399872,0.20317581295967,482,2,point,False,48275.25,0.84343463182449,4.1906170845032,symmetric,3000,0,0.78539816339745,4.0878224372864,0,False,0,False,False,point>
    # <Turnpoint None: Dobenreuth Halle,0.8673899769783,0.19440059363842,321,1,point,False,10597.842773438,3.0640232563019,0.84343463182449,symmetric,3000,0,0.78539816339745,0.38293236494064,0,False,0,False,False,finish>
    # <Turnpoint None: Burghfeuerstein,0.86904799938202,0.19420191645622,493,0,start,False,0,0,3.0640232563019,next,3000,0,0.78539816339745,3.0640232563019,0,False,0,False,False,start>

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
