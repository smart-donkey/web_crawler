# coding=utf-8

import json
import re
from openpyxl import Workbook

wb = Workbook()


patterns = [u'索尼', u'sony', u'x8500', u'x8566', u'x9300']
n_column = 2
st = wb.active
st['A1'] = 'topic'
st['B1'] = 'update_time'
st['C1'] = 'detail'

def output(c):
    print(c['content'])

def hit_conditions(content):
    all_targets = []
    if 'response_items' in content:
        all_targets = [detail['detail'] for detail in c['response_items']]
    all_targets.append(content['topic'])

    for target in all_targets:
        for pattern in patterns:
            p = re.compile(pattern, re.IGNORECASE)
            if re.search(p, target):
                return True

    return False

if __name__ == '__main__':
    with open('../amazon4.json', 'r') as f:
        data = json.load(f, encoding='utf-8')
        for c in data:
            output(c)


