import csv
import sqlite3
from contextlib import closing
from copy import deepcopy
from datetime import date
from pathlib import Path

from tqdm import tqdm


class Database:

    TABLE_NAME = 'train_data'
    DATABASE_FILE = 'train.db'

    def __init__(self):
        detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        self._connection = sqlite3.connect(self.DATABASE_FILE, detect_types=detect_types)
        self._connection.row_factory = sqlite3.Row

    def __del__(self):
        self._connection.close()

    def create(self):
        sql = """create table train_data (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    UPDATE_TIME DATE,
                    HOUR_ID INTEGER,
                    ZONE_CODE VARCHAR(10),
                    SERVER_NAME VARCHAR(20),
                    BANDWIDTH_TOTAL REAL,
                    MAX_USER INTEGER,
                    UNIQUE(UPDATE_TIME, HOUR_ID, ZONE_CODE, SERVER_NAME)
                )"""

        with self._connection, closing(self._connection.cursor()) as cur:
            cur.execute(sql)
            cur.execute('create index UPDATE_TIME_idx on train_data (UPDATE_TIME)')
            cur.execute('create index HOUR_ID_idx on train_data (HOUR_ID)')
            cur.execute('create index ZONE_CODE_idx on train_data (ZONE_CODE)')
            cur.execute('create index SERVER_NAME_idx on train_data (SERVER_NAME)')

        sql = """insert into train_data values (
                    :ID,
                    :UPDATE_TIME,
                    :HOUR_ID,
                    :ZONE_CODE,
                    :SERVER_NAME,
                    :BANDWIDTH_TOTAL,
                    :MAX_USER
            )"""
        with open('data/train.csv', 'r') as train_file, \
                self._connection, closing(self._connection.cursor()) as cur:
            reader = csv.DictReader(train_file)
            for index, row in enumerate(tqdm(reader), start=1):
                row['ID'] = index
                try:
                    cur.execute(sql, row)
                except sqlite3.IntegrityError:
                    pass

    def delete(self):
        self._connection.close()
        Path(self.DATABASE_FILE).unlink()
        self._connection = sqlite3.connect(self.DATABASE_FILE)
        self._connection.row_factory = sqlite3.Row

    def execute_sql(self, sql):
        with self._connection, closing(self._connection.cursor()) as cur:
            cur.execute(sql)
            return cur.fetchall()

    def filter(self, *args, **kwargs):
        kwargs = deepcopy(kwargs)
        where_clauses = []

        columns = ['UPDATE_TIME', 'HOUR_ID', 'ZONE_CODE', 'SERVER_NAME']
        for col in columns:
            values = kwargs.get(col)
            if values is None:
                continue
            if isinstance(values, list):
                for i, v in enumerate(values):
                    if isinstance(v, date):
                        values[i] = '\'{:%Y-%m-%d}\''.format(v)
                    if isinstance(v, str):
                        values[i] = '\'{}\''.format(v)
                where_clauses.append('{} in ({})'.format(col, ', '.join(values)))
            else:
                if isinstance(values, date):
                    values = '\'{:%Y-%m-%d}\''.format(values)
                if isinstance(values, str):
                    values = '\'{}\''.format(values)
                where_clauses.append('{} = {}'.format(col, values))

        where_clause = ''
        if len(where_clauses) > 0:
            where_clause = ' and '.join(where_clauses)
            where_clause = ' where ' + where_clause

        sql = 'select * from train_data ' + where_clause
        return self.execute_sql(sql)

    def list_servers(self):
        sql = 'select DISTINCT SERVER_NAME from train_data'
        rows = self.execute_sql(sql)
        return [row[0] for row in rows]

    def list_hours(self):
        sql = 'select DISTINCT HOUR_ID from train_data'
        rows = self.execute_sql(sql)
        return [row[0] for row in rows]

    def get_bandwidth_avg(self):
        sql = 'select avg(BANDWIDTH_TOTAL) from train_data'
        rows = self.execute_sql(sql)
        return rows[0][0]

    def get_max_user_avg(self):
        sql = 'select avg(MAX_USER) from train_data'
        rows = self.execute_sql(sql)
        return rows[0][0]
