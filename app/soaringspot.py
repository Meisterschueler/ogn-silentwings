from app.model import Contest, ContestClass, Contestant, Pilot, Task, Location, Turnpoint

import requests
from datetime import datetime


def check_soaringspot_time():
    time_url = 'http://api.soaringspot.com/v1/time'
    r = requests.get(time_url)
    server_time = datetime.strptime(r.headers['X-Server-Time'], '%A, %d-%b-%Y %H:%M:%S %Z')
    local_time = datetime.utcnow()
    time_delta = (local_time - server_time).total_seconds()

    if time_delta > 300:
        raise Exception('Local time and server time differ too much')


def get_soaringspot_auth_string(client_id, secret):
    import hashlib
    import hmac
    import ssl
    import random
    import base64

    nonce = base64.b64encode(ssl.RAND_bytes(random.randint(12, 30))).decode('utf-8')
    created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    data = nonce + created + client_id
    signature = base64.b64encode(hmac.new(secret.encode('utf-8'), msg=data.encode('utf-8'), digestmod=hashlib.sha256).digest()).decode('utf-8')
    auth_string = 'http://api.soaringspot.com/v1/hmac/v1 ClientID="{0}", Signature="{1}", Nonce="{2}", Created="{3}"' \
        .format(client_id, signature, nonce, created)

    return auth_string


def get_soaringspot_document(url, client_id, secret):
    from hal_codec import HALCodec

    auth_string = get_soaringspot_auth_string(client_id, secret)
    r = requests.get(url, headers={'Authorization': auth_string})
    codec = HALCodec()
    document = codec.load(r.text.encode('utf-8'))

    return document


def get_soaringspot_contests(url, client_id, secret):
    import math
    document = get_soaringspot_document(url, client_id, secret)
    print(document)
    contests = list()
    for item in document.items():
        if item[0] == "contests":
            for contest_row in item[1]:
                parameters = {'category': contest_row['category'],
                              'country': contest_row['country'],
                              'end_date': datetime.strptime(contest_row['end_date'], "%Y-%m-%d"),
                              'featured': contest_row['featured'],
                              'name': contest_row['name'],
                              'start_date': datetime.strptime(contest_row['start_date'], "%Y-%m-%d"),
                              'time_zone': contest_row['time_zone']}
                contest = Contest(**parameters)

                location_row = contest_row['location']
                parameters = {'altitude': location_row['altitude'],
                              'country': location_row['country'],
                              'latitude': math.degrees(location_row['latitude']),
                              'longitude': math.degrees(location_row['longitude']),
                              'name': location_row['name'],
                              'time_zone': location_row['time_zone']}
                location = Location(**parameters)
                contest.location = location

                for contest_class_row in contest_row['classes']:
                    parameters = {'category': contest_class_row['category'],
                                  'type': contest_class_row['type']}
                    contest_class = ContestClass(**parameters)
                    contest_class.contest = contest

                    contestants_doc = get_soaringspot_document(contest_class_row.links['contestants'].url, client_id, secret)
                    print(contestants_doc)
                    if 'code' in contestants_doc and contestants_doc['code'] == 404:
                        print("No contestant")
                    else:
                        for contestant_row in contestants_doc['contestants']:
                            parameters = {'aircraft_model': contestant_row['aircraft_model'],
                                          'aircraft_registration': contestant_row['aircraft_registration'],
                                          'club': contestant_row['club'] if 'club' in contestant_row else None,
                                          'contestant_number': contestant_row['contestant_number'],
                                          'handicap': contestant_row['handicap'],
                                          'live_track_id': contestant_row['live_track_id'],
                                          'name': contestant_row['name'],
                                          'not_competing': contestant_row['not_competing'],
                                          'pure_glider': contestant_row['pure_glider'],
                                          'sponsors': contestant_row['sponsors'] if 'sponsors' in contestant_row else None}
                            contestant = Contestant(**parameters)
                            contestant.contest_class = contest_class

                            for pilot_row in contestant_row['pilot']:
                                parameters = {'civl_id': pilot_row['civl_id'],
                                              'email': pilot_row['email'],
                                              'first_name': pilot_row['first_name'],
                                              'igc_id': pilot_row['igc_id'],
                                              'last_name': pilot_row['last_name'],
                                              'nationality': pilot_row['nationality']}
                                pilot = Pilot(**parameters)
                                pilot.contestant = contestant

                    tasks_doc = get_soaringspot_document(contest_class_row.links['tasks'].url, client_id, secret)
                    print(tasks_doc)
                    if 'code' in tasks_doc and tasks_doc['code'] == 404:
                        print("No task")
                    else:
                        for task_row in tasks_doc['tasks']:
                            parameters = {'images': task_row['images'],
                                          'no_start': datetime.strptime(task_row['no_start'], "%Y-%m-%dT%H:%M:%S"),
                                          'result_status': task_row['result_status'],
                                          'start_on_entry': task_row['start_on_entry'],
                                          'task_date': datetime.strptime(task_row['task_date'], "%Y-%m-%d"),
                                          'task_distance': task_row['task_distance'],
                                          'task_distance_max': task_row['task_distance_max'],
                                          'task_distance_min': task_row['task_distance_min'],
                                          'task_duration': task_row['task_duration'],
                                          'task_number': task_row['task_number'],
                                          'task_type': task_row['task_type'],
                                          'task_value': task_row['task_value']}
                            task = Task(**parameters)
                            task.contest_class = contest_class

                            points_doc = get_soaringspot_document(task_row.links['points'].url, client_id, secret)
                            print(points_doc)
                            if 'code' in points_doc and points_doc['code'] == 404:
                                print("No points")
                            else:
                                for point_row in points_doc['points']:
                                    parameters = {'name': point_row['name'],
                                                  'latitude': math.degrees(point_row['latitude']),
                                                  'longitude': math.degrees(point_row['longitude']),
                                                  'elevation': point_row['elevation'],
                                                  'point_index': point_row['point_index'],
                                                  'type': point_row['type'],
                                                  'multiple_start': point_row['multiple_start'],
                                                  'distance': point_row['distance'],
                                                  'course_in': point_row['course_in'],
                                                  'course_out': point_row['course_out'],
                                                  'oz_type': point_row['oz_type'],
                                                  'oz_radius1': point_row['oz_radius1'],
                                                  'oz_radius2': point_row['oz_radius2'],
                                                  'oz_angle1': math.degrees(point_row['oz_angle1']),
                                                  'oz_angle12': math.degrees(point_row['oz_angle12']),
                                                  'oz_angle2': math.degrees(point_row['oz_angle2']),
                                                  'oz_line': point_row['oz_line'],
                                                  'oz_max_altitude': point_row['oz_max_altitude'],
                                                  'oz_move': point_row['oz_move'],
                                                  'oz_reduce': point_row['oz_reduce'],
                                                  'speed_section_type': point_row['speed_section_type']}
                                    turnpoint = Turnpoint(**parameters)
                                    turnpoint.task = task

                contests.append(contest)

    return contests
