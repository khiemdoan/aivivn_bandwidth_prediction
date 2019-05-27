import csv
from pathlib import Path

from tqdm import tqdm


class Submission:

    def __init__(self):
        self._data = []

    def add_entry(self, test_id, bandwidth, max_user):
        entry = (test_id, round(bandwidth, 2), int(max_user))
        self._data.append(entry)

    def write(self, directory='output', filename='submission.csv'):
        output_dir = Path(__name__).parent / directory
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / filename
        with output_file.open('w', newline='') as csv_file:
            fieldnames = ['id', 'label']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for entry in tqdm(self._data):
                writer.writerow({'id': entry[0], 'label': '{} {}'.format(entry[1], entry[2])})
