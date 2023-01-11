from datetime import date, datetime
import os

if 'logs' not in os.listdir():
    os.mkdir('logs')


def text_log(message: str, curr_time=False,  show_console=False, filename=False):

    if not filename:
        filename = ('logs/Log ' + (date.today().strftime("%d/%m/%Y").replace('/', '-')) + '.txt')

    if not curr_time:
        curr_time = datetime.now().strftime("%H:%M:%S")

    with open(filename, 'a') as f:
        f.write(f'{curr_time} - {message} \n')

        if show_console:
            print(f'Saved log message {message} in {filename} at {curr_time} successfully.')


def clear_logs(location=False):

    if not location:
        os.chdir('logs/')

        for file in os.listdir():
            if file.endswith('.txt'):
                os.remove(file)
                print(f'Deleted file {file}')
