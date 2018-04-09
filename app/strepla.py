import requests
import json
from datetime import datetime
from app.model import Contest, ContestClass, Contestant, Pilot, Location


def list_strepla_contests():
    url = "http://www.strepla.de/scs/ws/competition.ashx?cmd=recent&daysPeriod=360"
    r = requests.get(url)
    json_data = json.loads(r.text.encode('utf-8'))

    print("\nID : Name of competition - Place of competition")
    print("=================================================================")
    for contest_row in json_data:
        print("{id}: {name} - {Location}".format(**contest_row))


def get_strepla_contest(competition_id):
    contest_url = "http://www.strepla.de/scs/ws/competition.ashx?cmd=info&cId=" + str(competition_id) + "&daysPeriod=360"
    r = requests.get(contest_url)
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
    contest_class_url = "http://www.strepla.de/scs/ws/compclass.ashx?cmd=overview&competition_id=" + str(competition_id)
    r = requests.get(contest_class_url)
    contest_class_data = json.loads(r.text.encode('utf-8'))

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

            parameters = {'first_name': contestant_row['name'].rsplit(',', 1)[0],
                          'last_name': contestant_row['name'].split(',', 1)[0],
                          'nationality': contestant_row['country']}
            pilot = Pilot(**parameters)
            pilot.contestant = contestant

    return contest



def get_strepla_class_task(competition_id,contest_class_name):
    # This function reads the tasks from a specific contest and class
    # TODO: Generate useful error message, if arguments are not provided
    all_task_url = "https://www.strepla.de/scs/ws/results.ashx?cmd=overviewDays&cID=" + str(competition_id) +  "&cc=" + str(contest_class_name)
    r = requests.get(all_task_url)
    all_task_data = json.loads(r.text.encode('utf-8'))
    for all_task_data_item in all_task_data:
        # print(task_data_item)
        print(all_task_data_item['idCD'],all_task_data_item['date'],all_task_data_item['state'])    
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
        for task_data_item in task_data:
            print(task_data_item)
    
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
