import requests
import re
from bs4 import BeautifulSoup

def get_prayers():
    url = 'https://m.awqaf.ae/prayertimes.aspx'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')

    content = []
    for row in soup.find_all('span'):
        content.append(row.text)

    prayers = content[5:-2]
    times = []
    names = prayers[0::2]
    for x in prayers:
        time = re.match('\d\d:\d\d', x)
        if time is not None:
            times.append(time.group(0))

    return zip(names, times)