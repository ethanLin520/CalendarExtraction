from icalendar import Calendar
from datetime import datetime
from dateutil.rrule import rrulestr

PATH = 'duedates.ics'

# Function to extract events
def extract_events():
    with open(PATH, 'r') as f:
        calendar_data = f.read()

    cal = Calendar.from_ical(calendar_data)
    events = []
    seen_events = set()

    for component in cal.walk():
        if component.name == "VEVENT":
            summary = str(component.get('summary'))
            dtstart = component.get('dtstart').dt
            date = component.get('dtend').dt

            # Check for recurrence rule
            if component.get('rrule'):
                rrule = rrulestr(str(component.get('rrule').to_ical().decode('utf-8')), dtstart=dtstart)
                for occurrence in rrule:
                    add_event(summary, occurrence, seen_events, events)
            else:
                events = add_event(summary, date, seen_events, events)
    return events

def add_event(summary, date, seen_events, events):
    event = {
        'task': summary,
        'date': date.strftime('%b %d'),
        'numeric': date.strftime('%m%d')
    }
    event_tuple = (event['task'], event['date'])
    if event_tuple not in seen_events:
        seen_events.add(event_tuple)
        events.append(event)
    return events

list = sorted(extract_events(), key=lambda x: x['numeric'])

# s1 = 'Task'
# print(f"{s1:<50}Date")
for t in list:
    print(f"{t['date']} {t['task']}", end='\n')
