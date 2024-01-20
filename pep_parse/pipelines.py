import csv
import time
from collections import defaultdict

from pep_parse.settings import BASE_DIR


class PepParsePipeline:
    def open_spider(self, spider):
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        timestapm = time.strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f'status_summary_{timestapm}.csv'
        file_path = results_dir / file_name
        self.file = open(file_path, 'w', encoding='utf-8')
        self.status_counter = defaultdict(int)

    def process_item(self, item, spider):
        self.status_counter[item['status']] += 1
        return item

    def close_spider(self, spider):
        results = [('Cтатус', 'Количество')]
        self.status_counter['Total'] = sum(self.status_counter.values())

        for status, amount in self.status_counter.items():
            results.append((status, amount))

        writer = csv.writer(self.file, dialect='unix')
        writer.writerows(results)
        self.file.close()
