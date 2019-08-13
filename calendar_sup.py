import json

def process(command: list=None) -> list:
    print('here')
    if command == None:
        return ['e', 'Error']
    if command[0] == 'goto':
        return go_to_month(command)
    if command[0] == 'add':
        add_event(command)
    return ['u', 'Unknown command']

def go_to_month(command: list) -> list:
    display_text = 'Now displaying ' + command[1] + ' ' + command[2]
    return ['c', display_text, int(command[1]), int(command[2])]

def add_event(command: list) -> list:
    if '-r' in command:
        return add_event_recursive(command)
    else:
        with open('months.json') as f:
            months_update = json.load(f)
        print(months_update)
        return


def add_event_recursive(command: list) -> list:
    return

def remove_event():
    return

def remove_event_recursive():
    return

