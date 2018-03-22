import os
from app import create_app, db
from app.model import Contest, ContestClass, Contestant, Pilot, Task, Beacon
from flask_migrate import Migrate, MigrateCommand
import click
from flask import request
from app.silent_wings import create_active_contests_string, create_contest_info_string, create_cuc
from app.soaringspot import get_soaringspot_contests
from app.routes import gencuc
from app.utils import logfile_to_beacons
from datetime import date

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db,
                Contest=Contest, ContestClass=ContestClass,
                Contestant=Contestant, Pilot=Pilot, Task=Task, Beacon=Beacon)


@app.cli.command()
def create_all():
    """Create the db."""
    db.create_all()


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def import_soaringspot():
    """Import data from SoaringSpot."""
    contests = get_soaringspot_contests(url=app.config['SOARINGSPOT_BASE_URL'],
                                        client_id=app.config['SOARINGSPOT_CLIENT_ID'],
                                        secret=app.config['SOARINGSPOT_SECRET'])
    db.session.add_all(contests)
    db.session.commit()


@app.cli.command()
@click.option('--logfile',  help='path of the logfile')
def import_logfile(logfile):
    """Import an OGN APRS stream logfile."""
    if logfile is None:
        print("You must specify the logfile with option '--logfile'")
        return

    print("Start importing logfile '{}'".format(logfile))
    beacons = logfile_to_beacons(logfile)
    db.session.add_all(beacons)
    db.session.commit()
    print("Inserted {} beacons".format(len(beacons)))


@app.cli.command()
def aprs_connect():
    """Run the aprs client."""
    from ogn.client import AprsClient
    client = AprsClient("Silent Wings Interface")
    client.connect()

    try:
        client.run(callback=lambda x: print(x), autoreconnect=True)
    except KeyboardInterrupt:
        print('\nStop ogn gateway')

    client.disconnect()

@app.cli.command()
@click.option('--contest',  help='Name of Contest')
def cmd_glidertracker_filter(contest):
    """Generate a filter list for glidertracker.org"""
    from app.glidertracker import glidertracker_filter, glidertracker_contests
    if contest is None:
        print("You must specify the name of the contest with option '--contest'")
        print("Following contests are known:")
        # Output list of known contests 
        print(glidertracker_contests())
        return

    print("Generating a filter list for glidertracker.org")
    glidertracker_filter(contest)

#########################
# Following Sections provides the Silent Wings Viewer interface
# For more details visit http://wiki.silentwings.no/index.php/Tracking_Protocol
#########################


@app.route("/getactivecontests.php")
def route_getactivecontests():
    # Parameters:
    # username=<user name>
    # cpassword=<encrypted password>
    # version=<version number>
    username = request.args.get('username', type=str)
    cpassword = request.args.get('cpassword', type=str)
    version = request.args.get('version', type=str)

    # Example request by SWV:
    # GET /getactivecontests.php?username=ogn&cpassword=ecbad38d0b5a3cf6482e661028b2c60c&version=1.3 HTTP/1.1

    # app.logger.error('getactivecontests.php was called: username = %s version = %s',username,version)

    # Expected return by SWV:
    # {contestname}FAIGP2005{/contestname}{contestdisplayname}1st FAI Grand PrixMondial{/contestdisplayname}{datadelay}15{/datadelay}{utcoffset}+01:00{/utcoffset}
    # {countrycode}FR{/countrycode}{site}St. Auban{/site}{fromdate}20050903{/fromdate}
    # {todate}20050912{/todate}{lat}44.1959{/lat}{lon}5.98849{/lon}{alt}{/alt}
    active_contests = create_active_contests_string()
    print(active_contests)
    return active_contests

@app.route("/getcontestinfo.php")
@app.route("/getcontestinfo")
def route_getcontestinfo():
    # Parameters:
    # username=<user name>
    # cpassword=<encrypted password>
    # contestname=<contest name>
    # date=<YYYYMMDD>
    username = request.args.get('username', type = str)
    cpassword = request.args.get('cpassword', type = str)
    contestname = request.args.get('contestname', type = str)
    date = request.args.get('date', type = str)

    if 'date' in request.args:
        # return CUC file
        print("create_cuc was called")
        return create_cuc(contestname,date)
    else:
        return create_contest_info_string(contestname)

@app.route("/gettrackerdata.php")
def route_gettrackerdata():
    # Parameters:
    # querytype=getintfixes
    # contestname=<contest name>
    # trackerid=<tracker id>
    # username=<user name>
    # cpassword=<encrypted password>
    # starttime=<YYYYMMDDHHMMSS>
    # endtime=<YYYYMMDDHHMMSS>
    # compression=<none | gzip>
    querytype = request.args.get('querytype', type = str)
    contestname = request.args.get('contestname', type = str)
    trackerid = request.args.get('trackerid', type = str)
    username = request.args.get('username', type = str)
    cpassword = request.args.get('cpassword', type = str)
    starttime = request.args.get('starttime', type = str)
    endtime = request.args.get('endtime', type = str)
    compression = request.args.get('compression', type = str)

    # GET /gettrackerdata.php?querytype=getintfixes&contestname=SOARINGSPOT3DTRACKINGINTERFACE%5f18METER&trackerid=FLRDDE1FC&username=ogn&cpassword=ecbad38d0b5a3cf6482e661028b2c60c&starttime=20180303000001&endtime=20180303235959&compression=gzip HTTP/1.0
    print("gettrackerdata was called!")
    return ""


@app.route("/getprotocolinfo.php")
def route_getprotocolinfo():
    from time import time
    username = request.args.get('username', type = str)
    cpassword = request.args.get('cpassword', type = str)
    # {version}1.3{/version}{date}20080811{/date}{time}1218457469{/time}
    return "{version}1.3{/version}{date}" + date.today().strftime("%Y%m%d") + "{/date}{time}" + str(int(time())) + "{/time}"



#########################
# Following Sections provides the Silent Wings Studio interface
# For more details visit https://github.com/swingsopen/swtracking/wiki/Tracking-Protocol
#########################

