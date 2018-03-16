import os
from app import create_app, db
from app.model import Contest, ContestClass, Contestant, Pilot, Task
from flask_migrate import Migrate, MigrateCommand
import click
from flask import request
from app.silent_wings import create_active_contests_string, create_contest_info_string
from app.soaringspot import get_soaringspot_contests


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db,
                Contest=Contest, ContestClass=ContestClass,
                Contestant=Contestant, Pilot=Pilot, Task=Task)


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
@click.option('--logfile', default=None, help='path of the logfile')
def import_logfile(logfile_name):
    """Import data from the ogn APRS stream."""
    print("Schlürf %s" % logfile_name)


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

    return create_active_contests_string()

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
        app.logger.error('Date was provided in URL; Should return CUC file')
        # return CUC file
        # Call function, which creates CUC file here
        return ""
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

    return ""

#########################
# Following Sections provides the Silent Wings Studio interface
# For more details see https://github.com/swingsopen/swtracking/wiki/Tracking-Protocol
#########################

