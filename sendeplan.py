from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
from pytz import timezone
import simplejson as json
import requests
import re


shoutedfm = "http://www.shouted.fm{link}"
sendeplanurl = shoutedfm.format(link="/index.php?area={area}&module=sendeplan")
notempty = re.compile(".+")


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")


def event_from_cell(cell):
    try:
        links = cell.find_all('a', attrs={"title": notempty})
        title = links[0].attrs['title']
        if title.find("Nonstop") != -1:
            return None
        return {
            "link": links[0].attrs["href"],
            "start_time": title.split(' - ')[0],
            "end_time": title.split(' - ')[1].split(' Uhr:')[0],
            "event_title": "{0}".format(title.split(' Uhr:')[1])
        }
    except:
        return None


def events_from_row(row):
    events = []
    for cell in row.find_all('td', attrs={"class": "content"}):
        event = event_from_cell(cell)
        if event:
            events.append(event)
    return events


def events_from_sendeplan(page):
    calendar = page.select('body table table')[2]
    events = []
    for i, row in enumerate(calendar.find_all('tr')):
        if i == 0:
            continue
        events += events_from_row(row)
    return events


def weekday_from_eventpage(page):
    calendar = page.select('body table table')[1]
    cell = calendar.find_all('td', attrs={'class': 'content'})[0]
    eventinfo = str(cell.b)
    de_weekdays = [
        "Montag",
        "Dienstag",
        "Mittwoch",
        "Donnerstag",
        "Freitag",
        "Samstag",
        "Sonntag"
    ]
    for i, wd in enumerate(de_weekdays):
        if eventinfo.find(wd) != -1:
            return i
    return -1


def fetch(url, **kwargs):
    response = requests.get(url.format(**kwargs))
    if response.status_code != 200:
        raise Exception("Can't connect")
    return response.text


def datetime_from_event(event):
    eventdate = datetime.now().replace(hour=int(event["start_time"].split(':')[0]), minute=int(event["start_time"].split(':')[1]), second=0, microsecond=0, tzinfo=timezone("Europe/Berlin"))
    eventdate += timedelta(days=eventdate.weekday() - event["weekday"])
    return eventdate


def duration_from_event(event):
    if event["end_time"].split(':')[1] != event["start_time"].split(':')[1]:
        raise Exception("not implemented yet")
    return (int(event["end_time"].split(':')[0]) - int(event["start_time"].split(':')[0])) * 60
        

def main():
    soup = BeautifulSoup(fetch(sendeplanurl, area="house"), 'html.parser')
    events = events_from_sendeplan(soup)
    for event in events:
        soup = BeautifulSoup(fetch(shoutedfm.format(link=event["link"])), 'html.parser')
        event["weekday"] = weekday_from_eventpage(soup)
        event["datetime"] = datetime_from_event(event)
        event["duration"] = duration_from_event(event)

    print(json.dumps(events, default=json_serial))


if __name__ == "__main__":
    main()
