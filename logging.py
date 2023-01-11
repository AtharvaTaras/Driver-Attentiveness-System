from datetime import date, datetime
import os

if 'logs' not in os.listdir():
    os.mkdir('logs')

filename = ('logs/ ' + (date.today().strftime("%d/%m/%Y").replace('/', '-')) + '.txt')
current_time = datetime.now().strftime("%H:%M:%S")

message = 'Test Log'

with open(filename, 'a') as f:
    f.write(f'{current_time} --- {message} \n')
