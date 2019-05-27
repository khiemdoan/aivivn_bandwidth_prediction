import csv
import itertools
from datetime import date, datetime

from tqdm import tqdm

from database import Database
from model import Model
from result import Result
from submission import Submission
from utils import week_range


if __name__ == '__main__':
    db = Database()

    start_date_train = date(2017, 10, 1)
    end_date_train = date(2019, 3, 10)

    start_date_predict = date(2019, 3, 9)
    end_date_predict = date(2019, 4, 10)

    weekdays = [i for i in range(7)]
    hours = db.list_hours()
    servers = db.list_servers()

    result = Result()
    default_bandwidth = db.get_bandwidth_avg()
    default_max_user = db.get_max_user_avg()
    result.set_default(default_bandwidth, default_max_user)

    total_iteration = len(weekdays) * len(hours) * len(servers)

    print('Train...')
    pbar = tqdm(total=total_iteration)
    for weekday, hour, server in itertools.product(weekdays, hours, servers):
        pbar.update(1)

        dates_train = list(week_range(start_date_train, end_date_train, weekday))
        
        data = db.filter(UPDATE_TIME=dates_train, HOUR_ID=hour, SERVER_NAME=server)
        if len(data) == 0:
            continue

        x_train = [row['UPDATE_TIME'] for row in data]
        y1_train = [row['BANDWIDTH_TOTAL'] for row in data]
        y2_train = [row['MAX_USER'] for row in data]
        dates_predict = list(week_range(start_date_predict, end_date_predict, weekday))

        model = Model()
        model.fit(x_train, y1_train, y2_train)
        y1_predict, y2_predict = model.predict(dates_predict)

        for date, y1, y2 in zip(dates_predict, y1_predict, y2_predict):
            result.add(date, hour, server, y1, y2)

    pbar.close()
    print()

    submission = Submission()

    print('Prepare submission...')
    with open('data/test_id.csv', 'r') as test_file:
        reader = csv.DictReader(test_file)
        for row in tqdm(reader):
            test_id = row['id']
            update_time = datetime.strptime(row['UPDATE_TIME'], '%Y-%m-%d').date()
            hour = int(row['HOUR_ID'])
            server = row['SERVER_NAME']
            bandwidth, max_user = result.get(update_time, hour, server)
            submission.add_entry(test_id, bandwidth, max_user)
    print()

    print('Start write submission...')
    submission.write()
