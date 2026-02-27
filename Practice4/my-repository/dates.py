#Напишите программу на Python, которая вычитает пять дней из текущей даты.
from datetime import date,timedelta
today = date.today()
new_date = today - timedelta(days=5)
print(new_date)


#Напишите программу на Python, которая выведет на экран вчера, сегодня и завтра.
from datetime import date,timedelta
today = date.today()
yestarday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print("Today:",today)
print("Yesterday:",yestarday)
print("Tomorrow:",tomorrow)


#Напишите программу на Python для удаления микросекунд из даты и времени.
from datetime import datetime
dt = datetime.now()
dt_no_micro = dt.replace(microsecond=0)
print("Result:",dt_no_micro)


#Напишите программу на Python для вычисления разницы между двумя датами в секундах.
from datetime import datetime
a = datetime.fromisoformat(input().strip())
b = datetime.fromisoformat(input().strip())
print(int((b - a).total_seconds()))