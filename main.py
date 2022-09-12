import requests
from icalendar import Calendar, Event, vDatetime
from datetime import datetime, timedelta
import os


SEASON_ID = "1084"
TEAM_NAME = "Seattle Dogs"

url = f"https://api.codetabs.com/v1/proxy/?quest=http://snokingpondhockey.com/api/game/list/{SEASON_ID}/0/0"
response = requests.get(url)
fullSchedule = response.json()
scriptPath = os.path.dirname(__file__)

try:        
    g = open(f'{scriptPath}/pondhockey.ics','rb')
    cal = Calendar.from_ical(g.read())
    lastDate = datetime.strptime(cal.walk()[-1].decoded('dtstart'), "%Y-%m-%dT%H:%M:%S")
    g.close()
except:
    lastDate = datetime.now()
    cal = Calendar()
    cal.add('prodid', f'{TEAM_NAME} Schedule')
    cal.add('version', '2.0')

for game in fullSchedule:
    if game['teamAwayName'] == TEAM_NAME or game['teamHomeName'] == TEAM_NAME:
        date = datetime.strptime(game['dateTime'], "%Y-%m-%dT%H:%M:%S")
        if date > lastDate:
            event = Event()
            event.add('summary', f"Pond Hockey")
            event.add('description', f"{game['teamAwayName']} @ {game['teamHomeName']}")
            event.add('dtstart', vDatetime(date))
            event.add('dtend', vDatetime(date + timedelta(hours=1)))
            cal.add_component(event)


g = open(f'{scriptPath}/pondhockey.ics','wb')
g.write(cal.to_ical())
g.close()