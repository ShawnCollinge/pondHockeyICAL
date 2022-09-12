import requests
from icalendar import Calendar, Event, vDatetime
from datetime import datetime, timedelta
import os


SEASON_ID = "1084"
TEAM_ID = "2502"
TEAM_NAME = "Seattle Dogs"

#url = f"https://api.codetabs.com/v1/proxy/?quest=http://snokingpondhockey.com/api/game/list/{SEASON_ID}/0/0"
url = f'https://api.codetabs.com/v1/proxy/?quest=https://snokinghockeyleague.com/api/game/list/{SEASON_ID}/0/{TEAM_ID}'
response = requests.get(url)
fullSchedule = response.json()
scriptPath = os.path.dirname(__file__)

try:        
    g = open(f'{scriptPath}/pondhockey.ics','rb')
    cal = Calendar.from_ical(g.read())
    lastDate = datetime.strptime(cal.walk()[-1].decoded('dtstart'), "%Y-%m-%dT%H%M%S")
    g.close()

except:
    lastDate = datetime.now()
    cal = Calendar()
    cal.add('prodid', f'-//Pond hockey/cal//CAL v1.0//EN')
    cal.add('version', '2.0')
    cal.add('method', "PUBLISH")
    cal.add('calscale', 'GEORGIAN')
    cal.add('x-wr-timezone', 'America/Los_Angeles')
    cal.add('x-wr-calname', "Pond hockey calendar")
    cal.add('x-wr-caldesk', 'Pond hockey calendar')


for game in fullSchedule:
    date = datetime.strptime(game['dateTime'], "%Y-%m-%dT%H:%M:%S")
    if date > lastDate:
        event = Event()            
        event.add('dtstart', vDatetime(date))
        event.add('dtend', vDatetime(date + timedelta(hours=1)))
        event.add('dtstamp', vDatetime(datetime.now()))
        event.add('class', 'PUBLIC')
        event.add('summary', f"Pond Hockey")
        event.add('description', f"{game['teamAwayName']} @ {game['teamHomeName']}")
        event.add('priority', 5)
        event.add('uid', f"{game['id']}.{SEASON_ID}@pondhockey")
        event.add('created', vDatetime(datetime.now()))
        event.add('last-modified', vDatetime(datetime.now()))
        cal.add_component(event)


g = open(f'{scriptPath}/pondhockey.ics','wb')
g.write(cal.to_ical())
g.close()