#!/usr/bin/env python3

import boto3
import json
from pprint import pprint

client = boto3.client('pricing')
paginator = client.get_paginator('get_products')

prices = []

filter_list = [
    ('capacitystatus', 'Used'),
    ('currentGeneration', 'Yes'),
    ('licenseModel', 'No License required'),
    ('marketoption', 'OnDemand'), 
    ('operatingSystem', 'Linux'),
    ('preInstalledSw', 'NA'),
    ('processorArchitecture', '64-bit'),
    ('regionCode', 'us-east-1'),
    ('tenancy', 'Shared'),
]

response_iterator = paginator.paginate(
    ServiceCode='AmazonEC2',
    FormatVersion='aws_v1',
    PaginationConfig={
        # 'MaxItems': 20,
    },
    Filters= list(
        map(
        lambda x: {
          'Type': 'TERM_MATCH',
          'Field': x[0],
          'Value': x[1]
        },
        filter_list
      )
    )

    # Filters=[
    #     {
    #         'Field':'regionCode',
    #         'Type':'TERM_MATCH',
    #         'Value':'us-east-1'
    #     },
    #     {
    #         'Field':'operatingSystem',
    #         'Type':'TERM_MATCH',
    #         'Value':'Linux'
    #     },
    # ]

)

for page in response_iterator:
    for price_data in page['PriceList']:
        prices.append(json.loads(price_data))

# with open('output.html', 'w') as _out:
#     _out.write('<!DOCTYPE html>')
#     _out.write("\n")
#     _out.write('<html><head><style>body { background-color: #222; color: #799 }</style></head><body><table><tbody>')
#     for price in prices:
#         _out.write("\n<tr><td>")
#         _out.write(price['product']['attributes']['instanceType'])
#         _out.write("</td><td>")
#         _out.write(price['product']['attributes']['operatingSystem'])
#         _out.write("</td><td>")
#         _out.write(price['product']['attributes']['regionCode'])
#         _out.write("</td><td>")
#         _out.write(price['product']['attributes']['vcpu'])
#         _out.write("</td><tr>")
#     _out.write('</tbody></table></body></html>')


    # print(price['product']['attributes'])
    ## for attribute in price['product']['attributes']:
        # print(attribute['instanceType'])


    # for service in page['Services']:
    #     services.append(service)
    #     # print(service)

with open('data.json', 'w') as _json_file:
    json.dump(prices, _json_file, sort_keys=True, indent=2)

#     for item in sorted(services, key=lambda x: x['ServiceCode'].lower()):
#         _out.write(f"<ul><li><div>{item['ServiceCode']}</div><ul>")
#         _out.write("\n")
#         for attribute in sorted(item['AttributeNames'], key=lambda x: x.lower()): 
#             _out.write(f"<li>{attribute}</li>")
#         _out.write("\n")
#         _out.write("</ul></ul>")
#         _out.write("\n")



