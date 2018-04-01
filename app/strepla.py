# flake8: noqa
import urllib.request, json

def get_strepla_contests_info():
    i = 0
    with urllib.request.urlopen("https://www.strepla.de/scs/ws/competition.ashx?cmd=recent&daysPeriod=360") as url:
        data = json.loads(url.read().decode())
        while i < len(data):
            data_dict = data[i]
            print(str(data_dict['id']) + ": " + str(data_dict['name']) + " - " + str(data_dict['Location']))
            i += 1

def get_strepla_contest(cID):
    with urllib.request.urlopen("https://www.strepla.de/scs/ws/competition.ashx?cmd=info&cId=" + str(cID) + "&daysPeriod=360") as url:
        data = json.loads(url.read().decode())[0]
        print(data)

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

