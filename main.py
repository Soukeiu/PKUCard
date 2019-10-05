from requests import Session
from random import random
from json import dump
from csv import DictWriter
from re import search

import config

with Session() as s:
    r = s.post('https://card.pku.edu.cn/cassyno/index', data={
        'errorcode': 1,
        'continueurl': '',
        'ssoticketid': config.user_name
    })
    print(r.text)
    r = s.post('https://card.pku.edu.cn/Page/Page', data={
        'flowID': 15,
        'type': 1,
        'apptype':  2,
        'Url': '%23',
        'MenuName': '流水查询',
        'EMenuName': '流水查询',
    })
    print(r.text)
    account = search(r"var acc = '(\d+)'", r.text).group(1)
    with open(config.output_file_name+'.json', 'w', encoding='utf-8') as f:
        data = []
        i = 1
        while True:
            r = s.post('https://card.pku.edu.cn/Report/GetPersonTrjn', data={
                'sdate': config.start_date,
                'edate': config.end_date,
                'account': account,
                'page': i,
            })
            print(r.text)
            json_data = r.json()
            data.extend(json_data['rows'])
            total = json_data['total']
            dump(json_data, f, ensure_ascii=False, indent=4)
            if i >= (total // 15) + (total % 15 > 0):
                break
            i += 1


fields = data[0].keys()
with open(config.output_file_name+'.csv', 'w', encoding='utf-8-sig',
          newline='') as f:
    writer = DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for rec in data:
        rec['MERCNAME'] = rec['MERCNAME'].strip()
        rec['TRANNAME'] = rec['TRANNAME'].strip()
        print(rec)
        writer.writerow(rec)
