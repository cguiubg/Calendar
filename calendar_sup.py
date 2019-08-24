import json
import datetime

def process(command: list=None) -> list:
    if command == None:
        return ['e', 'Error']
    if command[0] == 'goto':
        return go_to_month(command)
    if command[0] == 'add':
        return add_event(command)
    if command[0] == 'rm':
        return remove_event(command)
    return ['u', 'Unknown command']

def go_to_month(command: list) -> list:
    display_text = 'Now displaying ' + command[1] + ' ' + command[2]
    return ['c', display_text, int(command[1]), int(command[2])]

#Add an event into calendar with following format:
#add YYYY MM DD event

def add_event(command: list) -> list:
    with open('./months.json') as f:
        months_update = json.load(f)
    event = command[4]
    day = command[3]
    month = int(command[2])
    year = int(command[1])
    date = datetime.datetime(year, month, 1)
    month = date.strftime('%B')
    year = date.strftime('%Y')
    if day in months_update[month]['years'][year]:
        months_update[month]['years'][year][day].append(event)
    else:
        months_update[month]['years'][year][day] = [event]
    with open('./months.json', 'w') as f:
        json.dump(months_update, f, indent=4)
    return ['a', 'Added event: ' + event]

def remove_event(command: list) -> list:
    with open('./months.json') as f:
        months_update = json.load(f)
    event = command[4]
    day = command[3]
    month = int(command[2])
    year = int(command[1])
    date = datetime.datetime(year, month, 1)
    month = date.strftime('%B')
    year = date.strftime('%Y')
    if day in months_update[month]['years'][year]:
        if event in months_update[month]['years'][year][day]:
            months_update[month]['years'][year][day].remove(event)
        else:
            return ['e', 'Event not found']
    else:
        return ['e', 'Event not found']
    with open('./months.json', 'w') as f:
        json.dump(months_update, f, indent=4)
    return ['r', 'Removed event: ' + event]
