def tCO2e_to_MteCO2e(value):
    value = value.replace(',', '').strip()
    return float(value)/10**6

def as_is(value):
    return float(value)

datasheets = [
    {
        'name': 'BP',
        'reports':{
            2019: 'https://www.bp.com/content/dam/bp/business-sites/en/global/corporate/pdfs/sustainability/bp-esg-datasheet-2019.pdf',
        },
        'metrics': {
            'greenhouse gas emissions': {
                'regex': 'Operational control.{1,10}Scope 1 \(direct\) greenhouse gas emissions.*?(\d+\.\d+)\n',
                'unit': 'MteCO2e',
                'convert': as_is
            }
        }
    },
    {
        'name': 'Google',
        'reports':{
            2019: 'https://services.google.com/fh/files/misc/google_2019-environmental-report.pdf',
        },
        'metrics': {
            'greenhouse gas emissions': {
                'regex': 'Greenhouse gas emissions.{1,1000}Total.{1,100}\s([\d\,\.]+)\d{2}\n',
                'unit': 'MteCO2e',
                'convert': tCO2e_to_MteCO2e
            }
        }
    }
]

import os
import re
import requests

for datasheet in datasheets:
    print('Company name: %s' % datasheet['name'])

    for year, report_url in datasheet['reports'].items():
        print('', 'Report of %d: %s' % (year, report_url))

        r = requests.get(report_url)  
        with open(r'temp.pdf', 'wb') as pdf:
            pdf.write(r.content)
            print(' ', 'Downloaded %d bytes' % len(r.content))

        os.system('pdftotext temp.pdf temp.txt -raw')

        text = open('temp.txt').read()

        for metric_name, metric_meta in datasheet['metrics'].items():
            value = re.findall(metric_meta['regex'], text, re.I | re.S | re.M)[0]
            if metric_meta['convert']:
                value = metric_meta['convert'](value)
            print(' ', metric_name, '%.2f' % value, metric_meta['unit'])
