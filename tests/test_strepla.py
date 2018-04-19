import unittest
from unittest import mock

from app import create_app, db
from app.strepla import list_strepla_contests, get_strepla_contest_body, get_strepla_class_tasks

from tests.helper import print_contest

"""-                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               l
This should be the raw data required to mock the tests.

http://www.strepla.de/scs/ws/competition.ashx?cmd=recent&daysPeriod=360
[{"id":448,"name":"Deutsche Meisterschaft der Club Klasse","Location":"Flugplatz Mönchsheide","description":"","firstDay":"2017-08-15T00:00:00","lastDay":"2017-08-26T00:00:00","optIsPublic":"True","fnLogo":"logo.png","numDaysClass":"7.00","short_name":"CLUB","numDays":"7"},{"id":412,"name":"Gliding Competition Grabenstetten 2017","Location":"Grabenstetten","description":"Qualifikationsmeisterschaften zur DM Junioren 2018- Standardklasse- Clubklasse","firstDay":"2017-08-05T00:00:00","lastDay":"2017-08-12T00:00:00","optIsPublic":"True","fnLogo":"logo.jpg","numDaysClass":"3.00","short_name":"STD","numDays":"4"},{"id":442,"name":"Gollenberg Cup 2017","Location":"SLP Stölln/Rhinow","description":"","firstDay":"2017-07-27T00:00:00","lastDay":"2017-08-03T00:00:00","optIsPublic":"True","fnLogo":"logo.jpg","numDaysClass":"4.00","short_name":"Std","numDays":"4"},{"id":394,"name":"Junioren-Qualifikationsmeisterschaft Achmer","Location":"Sonderlandeplatz Achmer","description":"","firstDay":"2017-07-17T00:00:00","lastDay":"2017-07-23T00:00:00","optIsPublic":"True","fnLogo":"logo.gif","numDaysClass":"4.00","short_name":"Club","numDays":"4"},{"id":397,"name":"Junioren-Quali Leverkusen","Location":"Leverkusen Flugplatz (EDKL)","description":"","firstDay":"2017-07-15T00:00:00","lastDay":"2017-07-22T00:00:00","optIsPublic":"True","fnLogo":"logo.png","numDaysClass":"4.00","short_name":"Club","numDays":"4"}]

http://www.strepla.de/scs/ws/competition.ashx?cmd=info&cId=400&daysPeriod=360
[{"id":400,"name":"DM Doppelsitzer- und Standardklasse 2017","Location":"Zwickau (EDBI)","description":"","firstDay":"2017-06-20T00:00:00","lastDay":"2017-07-01T00:00:00","optIsPublic":"True","fnLogo":"logo.png","numDaysClass":"6.00","short_name":"STD","numDays":"6"}]

http://www.strepla.de/scs/ws/compclass.ashx?cmd=overview&cID=400
[{"id":850,"name":"STD","rulename":"1000 Punkte"},{"id":862,"name":"DoSi","rulename":"1000 Punkte Handicap"}]

http://www.strepla.de/scs/ws/pilot.ashx?cmd=competitors&cId=400&cc=STD
[{"id":1,"name":"Althaus, Moritz","country":"RP","glider_name":"LS 8","glider_callsign":"D-4156","glider_index":"1.00","glider_cid":"JO","flarm_ID":"","logger1":"LXV-20OFL","logger2":"FLA-IIZ","logger3":"LXV-1VCFL","className":"STD"},{"id":2,"name":"Barniske, Christoph","country":"ST","glider_name":"LS 8 neo","glider_callsign":"D-3761","glider_index":"1.00","glider_cid":"8A","flarm_ID":"","logger1":"FLA-9OY","logger2":"LXV-4PSFL","logger3":"","className":"STD"},{"id":3,"name":"Belz, Andreas","country":"BW","glider_name":"Discus 2a","glider_callsign":"D-1180","glider_index":"1.00","glider_cid":"AB","flarm_ID":"","logger1":"LXV-6ZVFL","logger2":"LXV-1LJFL","logger3":"","className":"STD"},{"id":4,"name":"Biechele, Kilian","country":"BY","glider_name":"Ls 8 neo","glider_callsign":"D-3725","glider_index":"1.00","glider_cid":"M1","flarm_ID":"","logger1":"LXV-JJIFL","logger2":"LXV-7IAFL","logger3":"","className":"STD"},{"id":5,"name":"Boehlke, Florian","country":"BY","glider_name":"LS 8","glider_callsign":"D-8683","glider_index":"1.00","glider_cid":"868","flarm_ID":"","logger1":"LXV-JXPFL","logger2":"FLA-B20","logger3":"","className":"STD"}]
"""


class contest_response:
    # http://www.strepla.de/scs/ws/competition.ashx?cmd=recent&daysPeriod=360
    text = '[{"id":448,"name":"Deutsche Meisterschaft der Club Klasse","Location":"Flugplatz Mönchsheide","description":"","firstDay":"2017-08-15T00:00:00","lastDay":"2017-08-26T00:00:00","optIsPublic":"True","fnLogo":"logo.png","numDaysClass":"7.00","short_name":"CLUB","numDays":"7"},{"id":412,"name":"Gliding Competition Grabenstetten 2017","Location":"Grabenstetten","description":"Qualifikationsmeisterschaften zur DM Junioren 2018- Standardklasse- Clubklasse","firstDay":"2017-08-05T00:00:00","lastDay":"2017-08-12T00:00:00","optIsPublic":"True","fnLogo":"logo.jpg","numDaysClass":"3.00","short_name":"STD","numDays":"4"},{"id":442,"name":"Gollenberg Cup 2017","Location":"SLP Stölln/Rhinow","description":"","firstDay":"2017-07-27T00:00:00","lastDay":"2017-08-03T00:00:00","optIsPublic":"True","fnLogo":"logo.jpg","numDaysClass":"4.00","short_name":"Std","numDays":"4"},{"id":394,"name":"Junioren-Qualifikationsmeisterschaft Achmer","Location":"Sonderlandeplatz Achmer","description":"","firstDay":"2017-07-17T00:00:00","lastDay":"2017-07-23T00:00:00","optIsPublic":"True","fnLogo":"logo.gif","numDaysClass":"4.00","short_name":"Club","numDays":"4"},{"id":397,"name":"Junioren-Quali Leverkusen","Location":"Leverkusen Flugplatz (EDKL)","description":"","firstDay":"2017-07-15T00:00:00","lastDay":"2017-07-22T00:00:00","optIsPublic":"True","fnLogo":"logo.png","numDaysClass":"4.00","short_name":"Club","numDays":"4"}]'


class contest_detail_response:
    # http://www.strepla.de/scs/ws/competition.ashx?cmd=info&cId=400&daysPeriod=360
    text = '[{"id":400,"name":"DM Doppelsitzer- und Standardklasse 2017","Location":"Zwickau (EDBI)","description":"","firstDay":"2017-06-20T00:00:00","lastDay":"2017-07-01T00:00:00","optIsPublic":"True","fnLogo":"logo.png","numDaysClass":"6.00","short_name":"STD","numDays":"6"}]'


class contest_class_response:
    # http://www.strepla.de/scs/ws/compclass.ashx?cmd=overview&cID=400
    text = '[{"id":850,"name":"STD","rulename":"1000 Punkte"},{"id":862,"name":"DoSi","rulename":"1000 Punkte Handicap"}]'


class contestants_std_response:
    # http://www.strepla.de/scs/ws/pilot.ashx?cmd=competitors&cId=400&cc=STD
    text = '[{"id":1,"name":"Althaus, Moritz","country":"RP","glider_name":"LS 8","glider_callsign":"D-4156","glider_index":"1.00","glider_cid":"JO","flarm_ID":"","logger1":"LXV-20OFL","logger2":"FLA-IIZ","logger3":"LXV-1VCFL","className":"STD"},{"id":2,"name":"Barniske, Christoph","country":"ST","glider_name":"LS 8 neo","glider_callsign":"D-3761","glider_index":"1.00","glider_cid":"8A","flarm_ID":"","logger1":"FLA-9OY","logger2":"LXV-4PSFL","logger3":"","className":"STD"},{"id":3,"name":"Belz, Andreas","country":"BW","glider_name":"Discus 2a","glider_callsign":"D-1180","glider_index":"1.00","glider_cid":"AB","flarm_ID":"","logger1":"LXV-6ZVFL","logger2":"LXV-1LJFL","logger3":"","className":"STD"},{"id":4,"name":"Biechele, Kilian","country":"BY","glider_name":"Ls 8 neo","glider_callsign":"D-3725","glider_index":"1.00","glider_cid":"M1","flarm_ID":"","logger1":"LXV-JJIFL","logger2":"LXV-7IAFL","logger3":"","className":"STD"},{"id":5,"name":"Boehlke, Florian","country":"BY","glider_name":"LS 8","glider_callsign":"D-8683","glider_index":"1.00","glider_cid":"868","flarm_ID":"","logger1":"LXV-JXPFL","logger2":"FLA-B20","logger3":"","className":"STD"}]'


class contestants_dosi_response:
    # http://www.strepla.de/scs/ws/pilot.ashx?cmd=competitors&cId=400&cc=STD
    text = '[{"id":21,"name":"Schreyer, Stefan","country":"HE","glider_name":"ASG 32 Mi","glider_callsign":"D-KTPC","glider_index":"1.04","glider_cid":"32","flarm_ID":"","logger1":"LXV-7VKFL","logger2":"LXV-38TFL","logger3":"","className":"DoSi"},{"id":22,"name":"Schwehm, Bernd","country":"RP","glider_name":"ASG 32 Mi","glider_callsign":"D-KSFF","glider_index":"1.05","glider_cid":"63","flarm_ID":"","logger1":"LXV-7WKFL","logger2":"LXV-17UFL","logger3":"","className":"DoSi"},{"id":23,"name":"Sommer, Norbert","country":"HE","glider_name":"Arcus T","glider_callsign":"D-KHLB","glider_index":"1.04","glider_cid":"HLB","flarm_ID":"","logger1":"LXV-JZ2FL","logger2":"LXN-CQ7FL","logger3":"LXV-LSKFL","className":"DoSi"},{"id":24,"name":"Theisinger, Martin","country":"RP","glider_name":"Arcus M","glider_callsign":"D-KNJK","glider_index":"1.04","glider_cid":"JK","flarm_ID":"","logger1":"LXV-7H0FL","logger2":"LXV-14EFL","logger3":"","className":"DoSi"},{"id":25,"name":"Trapp, Steffen","country":"NW","glider_name":"Arcus M","glider_callsign":"D-KDUE","glider_index":"1.05","glider_cid":"1H","flarm_ID":"","logger1":"LXV-6RNFL","logger2":"FIL-20351","logger3":"","className":"DoSi"},{"id":26,"name":"Triebel, Serena","country":"BY","glider_name":"ASG 32 Mi","glider_callsign":"D-KBAS","glider_index":"1.05","glider_cid":"82","flarm_ID":"","logger1":"LXV-7W9FL","logger2":"LXN-NX9FL","logger3":"","className":"DoSi"},{"id":27,"name":"Unseld, Georg","country":"BW","glider_name":"Duo Discus XLT","glider_callsign":"D-KIUT","glider_index":"1.01","glider_cid":"UT","flarm_ID":"","logger1":"LXV-7IVFL","logger2":"LXV-1V1FL","logger3":"","className":"DoSi"},{"id":28,"name":"Viehmann, Thomas","country":"HE","glider_name":"Arcus M","glider_callsign":"D-KLWO","glider_index":"1.05","glider_cid":"TWO","flarm_ID":"","logger1":"LXV-1SGFL","logger2":"LXV-7UOFL","logger3":"","className":"DoSi"}]'


class task_class_response1:
    # http://www.strepla.de/scs/ws/pilot.ashx?cmd=competitors&cId=400&cc=STD
    text = '[{"DT_RowId": 1, "idCD": "5368", "date": "2017-06-11T00:00:00", "idCC": "850", "nameCC": "STD", "state": "0", "sState": "Ungeplant"}, {"DT_RowId": 6, "idCD": "5899", "date": "2017-06-18T00:00:00", "idCC": "850", "nameCC": "STD", "state": "30", "sState": "Vorläufige Wertung"}, {"DT_RowId": 8, "idCD": "5917", "date": "2017-06-20T00:00:00", "idCC": "850", "nameCC": "STD", "state": "50", "sState": "Endgültige Wertung"}, {"DT_RowId": 11, "idCD": "5935", "date": "2017-06-23T00:00:00", "idCC": "850", "nameCC": "STD", "state": "60", "sState": "Neutralisiert"}]'


class task_class_response2:
    # http://www.strepla.de/scs/ws/results.ashx?cmd=task&cID=400&idDay=5899&activeTaskOnly=true
    # idCD = 5899
    text = '{"activeTask": 6532, "tasks": [{"id": "6532", "name": "Tagesaufgabe A", "distance": "267 km", "numLegs": "3", "tps": [{"scoring": {"type": "LINE", "width": 20000}, "tp": {"id": "178684", "name": "AP Werdau Eisenbahnbruecke", "lat": 50.7166666666667, "lng": 12.3733333333333}}, {"scoring": {"type": "KEYHOLE", "radiusCylinder": 500, "radiusSector": 10000, "angle": 90}, "tp": {"id": "179026", "name": "Speichersdorf Bf", "lat": 49.87, "lng": 11.7758333333333}}, {"scoring": {"type": "KEYHOLE", "radiusCylinder": 500, "radiusSector": 10000, "angle": 90}, "tp": {"id": "179023", "name": "Sonneberg Bf", "lat": 50.355, "lng": 11.1683333333333}}, {"scoring": {"type": "CYLINDER", "radius": 5000}, "tp": {"id": "178672", "name": "Zwickau FP EDBI", "lat": 50.7033333333333, "lng": 12.4591666666667}}]}]}'


class task_class_response3:
    # http://www.strepla.de/scs/ws/results.ashx?cmd=task&cID=400&idDay=5917&activeTaskOnly=true
    # idCD = 5917
    text = '{"activeTask": 6553, "tasks": [{"id": "6553", "name": "Tagesaufgabe A", "distance": "361 km", "numLegs": "4", "tps": [{"scoring": {"type": "LINE", "width": 20000}, "tp": {"id": "178687", "name": "AP Zwickau West A72 BAB010", "lat": 50.6383333333333, "lng": 12.44}}, {"scoring": {"type": "KEYHOLE", "radiusCylinder": 500, "radiusSector": 10000, "angle": 90}, "tp": {"id": "178900", "name": "Marienberg Markt", "lat": 50.6508333333333, "lng": 13.1633333333333}}, {"scoring": {"type": "KEYHOLE", "radiusCylinder": 500, "radiusSector": 10000, "angle": 90}, "tp": {"id": "179023", "name": "Sonneberg Bf", "lat": 50.355, "lng": 11.1683333333333}}, {"scoring": {"type": "KEYHOLE", "radiusCylinder": 500, "radiusSector": 10000, "angle": 90}, "tp": {"id": "179038", "name": "Suhl Bf", "lat": 50.605, "lng": 10.6825}}, {"scoring": {"type": "CYLINDER", "radius": 5000}, "tp": {"id": "178672", "name": "Zwickau FP EDBI", "lat": 50.7033333333333, "lng": 12.4591666666667}}]}]}'


class TestDB(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @mock.patch('app.strepla.requests')
    def test_list_strepla_contests(self, requests_mock):
        requests_mock.get.side_effect = [contest_response]

        list_strepla_contests()

    @mock.patch('app.strepla.requests')
    def test_get_strepla_contest(self, requests_mock):
        requests_mock.get.side_effect = [contest_detail_response, contest_class_response, contestants_std_response, contestants_dosi_response]

        contest = get_strepla_contest_body(400)
        print_contest(contest)

    @mock.patch('app.strepla.requests')
    def test_get_strepla_class_task(self, requests_mock):
        requests_mock.get.side_effect = [task_class_response1, task_class_response2, task_class_response3]

        tasks = get_strepla_class_tasks(400, 'STD')
        print(tasks)
        for task in tasks:
            print(task)
        
        db.session.add_all(tasks)
        db.session.commit()


if __name__ == '__main__':
    unittest.main()
