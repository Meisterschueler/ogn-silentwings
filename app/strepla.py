import requests
import json
from datetime import datetime
from app.model import Contest, ContestClass, Contestant, Pilot, Task, Location, Turnpoint


def list_strepla_contests():
    url = "http://www.strepla.de/scs/ws/competition.ashx?cmd=recent&daysPeriod=360"
    r = requests.get(url)
    json_data = json.loads(r.text.encode('utf-8'))

    print("\nID : Name of competition - Place of competition")
    print("=================================================================")
    for contest_row in json_data:
        print("{id}: {name} - {Location}".format(**contest_row))

def get_strepla_contest(competition_id):
    from app.utils import ddb_import
    contest_url = "http://www.strepla.de/scs/ws/competition.ashx?cmd=info&cId=" + str(competition_id) + "&daysPeriod=360"
    # print(contest_url)
    r = requests.get(contest_url)
    # Test if contest is present
    if (len(r.text)) == 2:
        print("This contest does not exist. Error. Aborting ....")
        return
    
    contest_data = json.loads(r.text.encode('utf-8'))[0]
    
    # Process contest location and date info
    parameters = {'end_date': datetime.strptime(contest_data['lastDay'], "%Y-%m-%dT%H:%M:%S"),
                  'name': contest_data['name'],
                  'start_date': datetime.strptime(contest_data['firstDay'], "%Y-%m-%dT%H:%M:%S")}
    contest = Contest(**parameters)

    parameters = {'name': contest_data['Location']}
    location = Location(**parameters)
    contest.location = location

    # Process contest class info
    contest_class_url = "http://www.strepla.de/scs/ws/compclass.ashx?cmd=overview&cid=" + str(competition_id)
    # print(contest_class_url)
    r = requests.get(contest_class_url)
    contest_class_data = json.loads(r.text.encode('utf-8'))
    
    ddb_entries = ddb_import()

    for contest_class_row in contest_class_data:
        parameters = {'category': contest_class_row['rulename'],
                      'type': contest_class_row['name']}

        contest_class = ContestClass(**parameters)
        contest_class.contest = contest

        # Process pilots of class
        contestant_url = "http://www.strepla.de/scs/ws/pilot.ashx?cmd=competitors&cId=" + str(competition_id) + "&cc=" + str(contest_class_row['name'])
        r = requests.get(contestant_url)
        contestant_data = json.loads(r.text.encode('utf-8'))
        if (len(contestant_data) == 0):
            print("Class name not recognized. Aborting.")
            return

        for contestant_row in contestant_data:
            parameters = {'aircraft_model': contestant_row['glider_name'],
                          'aircraft_registration': contestant_row['glider_callsign'],
                          'contestant_number': contestant_row['glider_cid'],
                          'handicap': contestant_row['glider_index'],
                          'live_track_id': contestant_row['flarm_ID']}
            contestant = Contestant(**parameters)
            contestant.contest_class = contest_class
            
            # Do some checks of the live_track_id
            if parameters['live_track_id']:
                print("Live_track_id defined via StrePla API")
                # Check if live_track_id is also in OGN DDB
                if parameters['live_track_id'] in ddb_entries.keys():
                    if parameters['aircraft_registration'] == ddb_entries[parameters['live_track_id']]:
                        print("Live_track_id is also in OGN DDB. Registrations match. Plausible id.")
                    else:
                        print("Live_track_id is also in OGN DDB. Registrations DOES NOT match. Check id.")
                else:
                    print("Live_track_id is not in OGN DDB. Plausibility check not possible.")
            else:
                # Live_track_id not provided. Performing Lookup on OGN DDB.
                if contestant_row['glider_callsign'] in ddb_entries.values():
                    live_track_id = list(ddb_entries.keys())[list(ddb_entries.values()).index(contestant_row['glider_callsign'])]
                    print(parameters['aircraft_registration'], "Live_track_id not provided. OGN DDB lookup found: ", live_track_id)
                    parameters = {'live_track_id': live_track_id}
                else:
                    print(parameters['aircraft_registration'], "Aircraft registration not found in OGN DDB.")

            parameters = {'first_name': contestant_row['name'].rsplit(',', 1)[0],
                          'last_name': contestant_row['name'].split(',', 1)[0],
                          'nationality': contestant_row['country']}
            pilot = Pilot(**parameters)
            pilot.contestant = contestant

    return contest


def get_strepla_class_task(competition_id, contest_class_name):
    # This function reads the tasks from a specific contest and class
    # TODO: Generate useful error message, if arguments are not provided
    all_task_url = "https://www.strepla.de/scs/ws/results.ashx?cmd=overviewDays&cID=" + str(competition_id) + "&cc=" + str(contest_class_name)
    r = requests.get(all_task_url)
    all_task_data = json.loads(r.text.encode('utf-8'))
    tasks = list()
    for all_task_data_item in all_task_data:
        # print(task_data_item)
        print(all_task_data_item['idCD'], all_task_data_item['date'], all_task_data_item['state'])
        if int(all_task_data_item['state']) == 0:
            print("Task not planned for day " + all_task_data_item['date'] + ". Skipping.")
            continue

        if int(all_task_data_item['state']) == 60:
            print("Task neutralized for day " + all_task_data_item['date'] + ". Skipping.")
            continue

        task_url = "http://www.strepla.de/scs/ws/results.ashx?cmd=task&cID=" + str(competition_id) + "&idDay=" + str(all_task_data_item['idCD']) + "&activeTaskOnly=true"
        print(task_url)
        r = requests.get(task_url)
        task_data = json.loads(r.text.encode('utf-8'))
        print(task_data)
        for task_data_item in task_data['tasks']:
            # print(task_data_item)
            parameters = {'result_status': all_task_data_item['state'],
                          'task_date': datetime.strptime(all_task_data_item['date'], "%Y-%m-%dT%H:%M:%S"),
                          'task_distance': task_data_item['distance']}

            task = Task(**parameters)

            point_index = 0
            for tps in task_data_item['tps']:
                # print("=== tps ===")
                # print(tps)
                if tps['scoring']['type'] == 'LINE':
                    parameters = {'oz_line': tps['scoring']['width'],
                                  'type': tps['scoring']['type']}

                elif tps['scoring']['type'] == 'AAT SECTOR':
                    parameters = {'type': tps['scoring']['type'],
                                  'oz_radius1': tps['scoring']['radius'],
                                  'oz_angle1': tps['scoring']['radial1'],
                                  'oz_angle2': tps['scoring']['radial2']}

                elif tps['scoring']['type'] == 'KEYHOLE':
                    parameters = {'type': tps['scoring']['type'],
                                  'oz_radius1': tps['scoring']['radiusCylinder'],
                                  'oz_radius2': tps['scoring']['radiusSector'],
                                  'oz_angle1': tps['scoring']['angle']}

                    # print("Keyhole TP recognizes.")

                elif tps['scoring']['type'] == 'CYLINDER':
                    parameters = {'type': tps['scoring']['type'],
                                  'oz_radius1': tps['scoring']['radius']}

                    # print("Cylinder TP recognizes.")

                tp_parameters = {'name': tps['tp']['name'],
                                 'latitude': tps['tp']['lat'],
                                 'longitude': tps['tp']['lng'],
                                 'point_index': point_index}

                point_index += 1
                parameters.update(tp_parameters)
                turnpoint = Turnpoint(**parameters)
                # print("=== Turnpoint ===")
                # print(turnpoint)
                turnpoint.task = task

            # task.contest_class = contest_class
            # print(task)
            tasks.append(task)

    return tasks


# Get classes for a specific contest
# https://www.strepla.de/scs/ws/compclass.ashx?cmd=overview&competition_id=403
def get_strepla_contest_classes(cID):
    url = "http://www.strepla.de/scs/ws/compclass.ashx?cmd=overview&cID=" + str(cID)
    r = requests.get(url)
    data = json.loads(r.text.encode('utf-8'))

    for row in data:
        print(row)


def get_strepla_contestants(cID, cc=None):
    import urllib
    # Get contestants of entire competition
    # https://www.strepla.de/scs/ws/pilot.ashx?cmd=competitors&cId=403
    if cc is not None:
        ccc = cc[0]
        with urllib.request.urlopen("https://www.strepla.de/scs/ws/pilot.ashx?cmd=competitors&cId=" + str(cID) + "&cc=" + str(ccc)) as url:
            data = json.loads(url.read().decode())
            if (len(data) == 0):
                print("Class name not recognized. Aborting")
                return

            i = 0
            while i < len(data):
                data_dict = data[i]
                # print(data_dict)
                print(str(data_dict['glider_callsign']) + ": " + str(data_dict['logger1']) + " - " + str(data_dict['name']))
                i += 1

    # Get contestants of specific class
    # https://www.strepla.de/scs/ws/pilot.ashx?cmd=competitors&cId=403&cc=18m
    else:
        with urllib.request.urlopen("https://www.strepla.de/scs/ws/pilot.ashx?cmd=competitors&cId=" + str(cID)) as url:
            data = json.loads(url.read().decode())
            i = 0
            while i < len(data):
                data_dict = data[i]
                print(data_dict)
                i += 1

# Get List of contest days
# https://www.strepla.de/scs/ws/results.ashx?cmd=overviewDays&cID=403&cc=18m

# Get task of specific day of specific contest
# https://www.strepla.de/scs/ws/results.ashx?cmd=task&cID=400&idDay=5917&activeTaskOnly=false
