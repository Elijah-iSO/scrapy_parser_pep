import csv
import time
from collections import defaultdict

from pep_parse.settings import BASE_DIR


class PepParsePipeline:
    def open_spider(self, spider):
        timestapm = time.strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f'status_summary_{timestapm}.csv'
        self.results_dir = BASE_DIR / 'results'
        self.file_path = self.results_dir / file_name

        self.status_counter = defaultdict(int)

    def process_item(self, item, spider):
        self.status_counter[item['status']] += 1
        return item

    def close_spider(self, spider):
        self.status_counter['Total'] = sum(self.status_counter.values())

        results = [
            ('Cтатус', 'Количество'),
            *self.status_counter.items()
        ]

        self.results_dir.mkdir(exist_ok=True)

        with open(self.file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(results)
