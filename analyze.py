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
    print(c['topic'], c['update_time'])
    global n_column
    st['A' + str(n_column)] = c['topic']
    st['B' + str(n_column)] = c['update_time']
    print('=============================================================================')
    details = list()
    if 'response_items' in c:
        for detail in c['response_items']:
            detail_text = detail['detail'].strip()
            if detail_text and detail_text not in details:
                 details.append(detail['detail'])

        for detail in details:
            print(detail)
            st['C' + str(n_column)] = detail
            n_column += 1
    print('=============================================================================')


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
    with open('../comments_200_pages.json', 'r') as f:
        data = json.load(f, encoding='utf-8')
        for c in data:
            if hit_conditions(c):
                output(c)

    import datetime
    wb.save("jd-bbs" + datetime.datetime.now().strftime("%Y%m%d_%H%s") + ".xls")


