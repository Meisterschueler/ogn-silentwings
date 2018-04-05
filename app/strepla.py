# flake8: noqa
import urllib.request, json
from datetime import datetime
from app.model import Contest, ContestClass, Contestant, Pilot, Task, Location

def get_strepla_contests_info():
    i = 0
    with urllib.request.urlopen("http://www.strepla.de/scs/ws/competition.ashx?cmd=recent&daysPeriod=360") as url:
        data = json.loads(url.read().decode())
        print("\nID : Name of competition - Place of competition")
        print("=================================================================")
        while i < len(data):
            data_dict = data[i]
            print(str(data_dict['id']) + ": " + str(data_dict['name']) + " - " + str(data_dict['Location']))
            i += 1

def get_strepla_contest(cID):
    contests = list()
    # Process contest location and date info
    with urllib.request.urlopen("http://www.strepla.de/scs/ws/competition.ashx?cmd=info&cId=" + str(cID) + "&daysPeriod=360") as url:
        contest_data = json.loads(url.read().decode())[0]
        # print(contest_data)
        contest_dict = {'end_date': datetime.strptime(contest_data['lastDay'], "%Y-%m-%dT%H:%M:%S"),
                        'name': contest_data['name'],
                        'start_date': datetime.strptime(contest_data['firstDay'], "%Y-%m-%dT%H:%M:%S")}
        contest = Contest(**contest_dict)

        location_dict = {'name': contest_data['Location']}
        location = Location(**location_dict)
        contest.location = location

        # Process contest class info
        with urllib.request.urlopen("http://www.strepla.de/scs/ws/compclass.ashx?cmd=overview&cID=" + str(cID)) as url:
            class_data = json.loads(url.read().decode())
            for contest_class_row in class_data:
                # print("contest_class_row:\n", contest_class_row)
                contest_class_dict = {'category': contest_class_row['rulename'],
                                  'type': contest_class_row['name']}

                contest_class = ContestClass(**contest_class_dict)
                contest_class.contest = contest

                # print(contest_class_row['name'])
                # Process pilots of class
                # print("https://www.strepla.de/scs/ws/pilot.ashx?cmda=competitors&cId=" + str(cID) + "&cc=" + str(contest_class_row['name']))
                with urllib.request.urlopen("http://www.strepla.de/scs/ws/pilot.ashx?cmd=competitors&cId=" + str(cID) + "&cc=" + str(contest_class_row['name'])) as url:
                    pilot_data = json.loads(url.read().decode())
                    # print(pilot_data) 
                    if (len(pilot_data) == 0):
                        print("Class name not recognized. Aborting.")
                        return

                    for pilot_row in pilot_data:
                        # print(str(pilot_row['glider_callsign']) + ": " + str(pilot_row['logger1']) + " - " + str(pilot_row['name']))
                        # print(pilot_row)
                        contestant_dict = {'aircraft_model': pilot_row['glider_name'],
                                           'aircraft_registration' : pilot_row['glider_callsign'],
                                           'contestant_number': pilot_row['glider_cid'],
                                           'handicap': pilot_row['glider_index'],
                                           'live_track_id': pilot_row['flarm_ID']}
                        contestant = Contestant(**contestant_dict)
                        contestant.contest_class = contest_class

                        pilot_dict = {'first_name': pilot_row['name'].rsplit(',',1)[0],
                                      'last_name': pilot_row['name'].split(',',1)[0],
                                      'nationality': pilot_row['country']}
                        pilot = Pilot(**pilot_dict)
                        pilot.contestant = contestant

        contests.append(contest)

    return contests


# Get classes for a specific contest
# https://www.strepla.de/scs/ws/compclass.ashx?cmd=overview&cID=403
def get_strepla_contest_classes(cID):
    with urllib.request.urlopen("https://www.strepla.de/scs/ws/compclass.ashx?cmd=overview&cID=" + str(cID)) as url:
        data = json.loads(url.read().decode())
        i = 0
        while i < len(data):
            data_dict = data[i]
            print(data_dict)
            i += 1

def get_strepla_contestants(cID,*cc):
    # Get contestants of entire competition
    # https://www.strepla.de/scs/ws/pilot.ashx?cmd=competitors&cId=403
    if (len(cc) != 0):
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

