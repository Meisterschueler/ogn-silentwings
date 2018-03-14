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
