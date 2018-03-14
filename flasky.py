import os
from app import create_app, db
from app.model import Contest, ContestClass, Contestant, Pilot, Task
from flask_migrate import Migrate, MigrateCommand
import click
from flask import request
from app.silent_wings import create_active_contests_string
from app.seeyou_cloud import get_seeyou_cloud_contests_as_objects


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
def import_seeyou_cloud():
    """Import data from SeeYou Cloud."""
    objects = get_seeyou_cloud_contests_as_objects(url=app.config['NAVITER_BASE_URL'],
                                                   client_id=app.config['NAVITER_CLIENT_ID'],
                                                   secret=app.config['NAVITER_SECRET'])
    db.session.add_all(objects)
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
