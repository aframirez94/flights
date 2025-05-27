from datetime import datetime, timedelta
from typing import List, Dict

MAX_FLIGHT_CONNECTIONS = 2

class Event:
    def __init__(self, event_dict):
        self.flight_number = event_dict.get("flight_number")
        self.dep_city = event_dict.get("departure_city")
        self.arr_city = event_dict.get("arrival_city")
        self.dep_datetime = format_datetime(event_dict.get("departure_datetime"))
        self.arr_datetime = format_datetime(event_dict.get("arrival_datetime"))

    def get_dict(self):
        return {
            "flight_number": self.flight_number,
            "from": self.dep_city,
            "to": self.arr_city,
            "departure_time": datetime.strftime(self.dep_datetime, "%Y-%m-%d %H:%M:%S"),
            "arrival_time": datetime.strftime(self.arr_datetime, "%Y-%m-%d %H:%M:%S")
        }


def generate_valid_journeys(events, date, origin, destination):
    # Parse input date
    journeys = []
    for event in events:
        first_event = Event(event)
        # filter out by origin and date
        if first_event.dep_city != origin or first_event.dep_datetime.date() != date:
            continue

        # now let's evaluate if the destination is the same so it is a direct flight
        if first_event.arr_city == destination and is_valid_total_travel_time(first_event):
            journeys.append(
                {
                    "connections": 0,
                    "path": [first_event.get_dict()]
                }
            )
            continue

        #if not, it can be a connection flight
        for event2 in events:
            sec_event = Event(event2)

            # now lets look for an event that has the same destination
            if sec_event.arr_city != destination:
                continue

            # if the sec_event departure matches with the first event arrival and the others conditions, then append the event
            if (sec_event.dep_city == first_event.arr_city
                and is_valid_connection_time(first_event, sec_event)
                and is_valid_total_travel_time(first_event, sec_event)):

                journeys.append(
                {
                    "connections": 1,
                    "path": [first_event.get_dict(), sec_event.get_dict()]
                }
            )
            
    return journeys

def format_datetime(string_datetime):
    """
    formats a string datetime into datetime obj

    input: str datetime
    output: datetime obj
    """
    return datetime.strptime(string_datetime, "%Y-%m-%dT%H:%M:%S.%f%z")

def is_valid_total_travel_time(first_event, sec_event=None):
    if sec_event is None:
        return first_event.arr_datetime - first_event.dep_datetime <= timedelta(hours=24)
    return sec_event.arr_datetime - first_event.dep_datetime <= timedelta(hours=24)

def is_valid_connection_time(first_event, sec_event):
    return sec_event.dep_datetime - first_event.arr_datetime <= timedelta(hours=4)
