from app.model import Contest, Contestant
from app import db

def glidertracker_filter():
    # This file write a filter list for glidertracker
    # ID,CALL,CN,TYPE
    # 06DDABCD,D-ABCD,CD,DuoDiscus


    result_list = list()
    result_list.append("ID,CALL,CN,TYPE")

    for contestant in db.session.query(Contestant):
        pilot = contestant.pilots[0]

        entry_dict = {'live_track_id': contestant.live_track_id,
                      'aircraft_registration': contestant.aircraft_registration,
                      'contestant_number': contestant.contestant_number,
                      'aircraft_model': contestant.aircraft_model}

        entry = '"{live_track_id}","{aircraft_registration}","{contestant_number}","{aircraft_model}"'.format(**entry_dict)
        result_list.append(entry)

    return "\n".join(result_list)
