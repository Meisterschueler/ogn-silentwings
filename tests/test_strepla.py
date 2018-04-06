import unittest
from unittest import mock

from app import create_app, db
from app.strepla import list_strepla_contests, get_strepla_contest

from tests.helper import print_contest

"""
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

        contest = get_strepla_contest(400)
        print_contest(contest)


if __name__ == '__main__':
    unittest.main()
