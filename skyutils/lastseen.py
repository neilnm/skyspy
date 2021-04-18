import json
import math
from datetime import datetime

from bs4 import BeautifulSoup


def update_last_seen():
    with open('web/data.json') as f:
        data = json.load(f)

    last_ts = data['data']['ts']

    try:
        last_ts = datetime.strptime(last_ts, "%Y-%m-%d %H:%M")
        time_diff = (datetime.now() - last_ts).total_seconds()
        last_seen = get_text_to_display(time_diff)
    except ValueError:
        last_seen = "N/A"

    data['data']['lastSeen'] = last_seen

    with open('web/data.json', 'w') as f:
        json.dump(data, f)


def get_text_to_display(time):
    # convert to minutes
    time = math.floor(time / 60)

    # handling default starting time of 2020-1-1
    if time > 500000:
        return "N/A"

    if time == 0:
        return "Just now"

    if time == 1:
        return f"{time} minute ago"

    if time < 60:
        return f"{time} minutes ago"

    hours = math.floor(time / 60)
    minutes = time % 60
    return f"{hours}h{minutes:02d} minutes ago"


def update_data_ts():
    with open('web/data.json', 'r') as f:
        data = json.load(f)

    with open('web/data.json', 'w') as f:
        data['data']['dataTs'] = str(datetime.now().strftime("%Y-%m-%d %H:%M"))
        json.dump(data, f)


