from app.model import Contest, Contestant
from app import db


# This function generates the filter contents
def glidertracker_filter(contest_name_with_class_type):
    # ===============================================
    # This file write a filter list for glidertracker
    # ID,CALL,CN,TYPE
    # 06DDABCD,D-ABCD,CD,DuoDiscus
    # ==============================================
    contest_name = contest_name_with_class_type.partition("_")[0]
    short_name = contest_name.replace(" ", "").upper()
    contest_class_type = contest_name_with_class_type.partition("_")[2]

    print(contest_name)
    result_list = list()
    result_list.append("ID,CALL,CN,TYPE")

    for contest in db.session.query(Contest):
        for contest_class in contest.classes:
            if contest.name.replace(" ", "").upper() == short_name and contest_class.type.replace("_", "").replace("-", "").upper() == contest_class_type:
                print("This is our contest: " + contest_name)
                print("This is our class: " + contest_class_type)

                for contestant in db.session.query(Contestant):
                    # pilot = contestant.pilots[0]

                    entry_dict = {'live_track_id': contestant.live_track_id,
                                  'aircraft_registration': contestant.aircraft_registration,
                                  'contestant_number': contestant.contestant_number,
                                  'aircraft_model': contestant.aircraft_model}

                    entry = '"{live_track_id}","{aircraft_registration}","{contestant_number}","{aircraft_model}"'.format(**entry_dict)
                    result_list.append(entry)
    print("\n".join(result_list).replace('"', ""))
    return "\n".join(result_list)


# This function prints all available contests and classes
def glidertracker_contests():
    result_string = list()
    for contest in db.session.query(Contest):
        for contest_class in contest.classes:
            short_name = contest.name.replace(" ", "").upper() + "_" + contest_class.type.replace("_", "").replace("-", "").upper()
            # long_name = contest.name + " " + contest_class.type
            result_string.append(short_name)

    return "\n".join(result_string)
