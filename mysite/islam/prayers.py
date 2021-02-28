from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime, timedelta
from rest_framework import serializers


class Prayer:
    def __init__(self, englishname, arabicname, time):
        self.arabicname = arabicname
        self.englishname = englishname
        self.time = time


class PrayerSerializer(serializers.Serializer):
    englishname = serializers.CharField(max_length=100)
    arabicname = serializers.CharField(max_length=100)
    time = serializers.CharField(max_length=100)


def get_prayer():
    url = 'https://m.awqaf.ae/prayertimes.aspx'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')

    names = ['Al Fajr', 'Al Shurooq', 'Al Dhuhr', 'Al Asr', 'Al Maghreb', 'Al Esha']
    names1 = ['الفجر', 'الشروق', 'الظهر', 'العصر', 'المغرب', 'العشاء']
    prayers = []
    ul = soup.find('ul', {'data-role': 'listview'})

    for item, name, name1 in zip(ul.find_all('li'), names, names1):
        t = re.findall('\d+:\d+', item.text)
        tim = datetime.strptime(t[0], '%I:%M')
        p = Prayer(englishname=name, arabicname=name1, time=tim)
        prayers.append(p)

    for index, prayer in enumerate(prayers):
        if index == 2 or index == 3 or index == 4 or index == 5:
            prayer.time = prayer.time + timedelta(hours=12)

    for x in prayers:
        x.time = x.time.strftime('%H:%M')

    serializer = PrayerSerializer(prayers, many=True)

    return serializer.data


def month_def(months, m):
    for i, mon in enumerate(months):
        if i == (int(m.text) - 1):
            return months[i]


def get_date():
    url = 'https://m.awqaf.ae/prayertimes.aspx'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    day = soup.find('span', {'id': 'ContentPlaceHolder1_DataList1_HDayLabel_0'})
    month = soup.find('span', {'id': 'ContentPlaceHolder1_DataList1_HMonthLabel_0'})
    year = soup.find('span', {'id': 'ContentPlaceHolder1_DataList1_HYearLabel_0'})

    months = ['محرم', 'صفر', 'ربيع الأول', 'ربيع الثاني', 'جمادى الأولى', 'جمادى الآخرة', 'رجب', 'شعبان', 'رمضان',
              'شوال', 'ذو القعدة', 'ذو الحجة']

    m = month_def(months, month)
    return f'{day.text.strip()} - {m} - {year.text.strip()}'