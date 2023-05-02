import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

url = 'https://online.zakon.kz/accountant/Calendars/Holidays/2023#'

resp = requests.get(url, verify=False)

soup = BeautifulSoup(resp.content, 'html.parser')

parent_div = soup.find_all('div', {'class': 'd-flex flex-row week-row'})
dayweeks = [
    'Пн',
    'Вт',
    'Ср',
    'Чт',
    'Пт',
    'Сб',
    'Вс'
]
type = []
day = []

for parent in parent_div:
    sub_div = parent.find_all('div', {'class': 'calendar-day'})
    span = parent.find_all('span')
    ind = 0
    for sub in sub_div:
        type.append(sub.get('class'))
        day.append(str(span[ind].text).strip())
        ind += 1

month = 0
df = pd.DataFrame(columns=['Day', 'Weekday', 'Type'])
for i in range(len(day)):

    if 'masked' in type[i] and 'prev-month' in type[i]:
        continue
    if 'holiday' in type[i]:
        type[i] = 'Holiday'
    else:
        type[i] = 'Working'

    if day[i] == '1':
        month += 1

    if int(day[i]) < 10:
        day[i] = '0' + day[i]

    if month < 10:

        year = datetime.datetime.now().year
        date = datetime.date(year, int(month), int(day[i]))

        print(f'{day[i]}.0{month}', type[i], dayweeks[date.weekday()])
        row = {'Day': f'{day[i]}.0{month}.{str(year)[-2:]}', 'Weekday': dayweeks[date.weekday()], 'Type': type[i]}
        df.loc[len(df)] = row
    else:
        year = datetime.datetime.now().year
        date = datetime.date(year, int(month), int(day[i]))
        print(f'{day[i]}.{month}', type[i], dayweeks[date.weekday()])
        row = {'Day': f'{day[i]}.{month}.{str(year)[-2:]}', 'Weekday': dayweeks[date.weekday()], 'Type': type[i]}
        df.loc[len(df)] = row

df.to_excel(r'\\172.16.8.87\d\Dauren\Производственный календарь 2023.xlsx', index=False)