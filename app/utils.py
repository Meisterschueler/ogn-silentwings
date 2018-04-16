from datetime import date

# Imports OGN DDB into dict
def ddb_import():
    import requests
    import csv
    from io import StringIO
    ddb_url = "http://ddb.glidernet.org/download/"
    r = requests.get(ddb_url)
    rows = '\n'.join(i for i in r.text.splitlines() if i[0] != '#')
    data = csv.reader(StringIO(rows), quotechar="'", quoting=csv.QUOTE_ALL)

    ddb_entries = dict()
    for row in data:
        ddb_entries[row[1]] = row[3]
        
    return ddb_entries

def process_beacon(raw_message, reference_date=None):
    from ogn.parser import parse, ParseError
    if raw_message[0] != '#':
        try:
            message = parse(raw_message, reference_date)
        except NotImplementedError as e:
            print('Received message: {}'.format(raw_message))
            print(e)
            return None
        except ParseError as e:
            print('Received message: {}'.format(raw_message))
            print('Drop packet, {}'.format(e.message))
            return None
        except TypeError as e:
            print('TypeError: {}'.format(raw_message))
            return None
        except Exception as e:
            print(raw_message)
            print(e)
            return None

        if message['aprs_type'] == 'status' or message['beacon_type'] == 'receiver_beacon':
            return None
        else:
            subset_message = {k: message[k] for k in message.keys() & {'name', 'address', 'timestamp', 'latitude', 'longitude', 'altitude', 'track', 'ground_speed', 'climb_rate', 'turn_rate'}}
            return subset_message


def open_file(filename):
    """Opens a regular or unzipped textfile for reading."""
    import gzip
    f = open(filename, 'rb')
    a = f.read(2)
    f.close()
    if (a == b'\x1f\x8b'):
        f = gzip.open(filename, 'rt')
        return f
    else:
        f = open(filename, 'rt')
        return f


def logfile_to_beacons(logfile, reference_date=date(2015, 1, 1)):
    from .model import Beacon
    fin = open_file(logfile)
    beacons = list()
    for line in fin:
        message = process_beacon(line.strip(), reference_date=reference_date)
        if message is not None:
            beacon = Beacon(**message)
            beacons.append(beacon)

    fin.close()
    return beacons
