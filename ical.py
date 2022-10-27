from icalendar import Calendar
from datetime import datetime
import os

def is_time_between(begin_time, end_time, check_time=None):
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:
        return check_time >= begin_time or check_time <= end_time

def gather_ics(path="."):
    try:
        dir = os.listdir(f"{path}/calendars")
        return [f"{path}/calendars/{file}" for file in dir if os.path.isfile(f"{path}/calendars/{file}") and file.endswith(".ics")]
    except:
        raise FileNotFoundError(f"{path}/calendars folder not found.")
    
def read_ics(path):
    fd = open(path)
    cal = Calendar.from_ical(fd.read())
    fd.close()
    return cal
                        
def analyse_ics(ics_path, search="Amphi"):
    amphi_libres = []
    for path in ics_path:
        print(f"Retrieving data from '{path}'...")
        cal = read_ics(path)
        for c in cal.walk():
            if c.name == "VEVENT":
                start,end = c.get("dtstart").dt, c.get("dtend").dt
                loc = c.get("location")
                if start.date() == datetime.now().date():
                    print(datetime.now().time())
                    if is_time_between(start.time(), end.time()):
                        amphi_libres.append(str(loc))
    print(amphi_libres)
                    
analyse_ics(gather_ics())