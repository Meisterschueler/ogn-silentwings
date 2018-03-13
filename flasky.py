import os
from app import create_app, db
from app.model import Contest, ContestClass, Contestant, Pilot, Task
from flask_migrate import Migrate, MigrateCommand
import click

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db,
                Contest=Contest, ContestClass=ContestClass,
                Contestant=Contestant, Pilot=Pilot, Task=Task)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def import_naviter():
    """Import data from SeeYou Cloud."""
    print('moin moin!')


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
