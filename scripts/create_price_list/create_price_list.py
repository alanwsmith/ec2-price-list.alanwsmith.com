#!/usr/bin/env python3

import json
import re

from string import Template

with open('../get_raw_price_data/data.json') as _json:
    raw_data = json.load(_json)

products = []

gpu_names = {
    'p4d': 'NVIDIA A100 Tensor Core',
    'p4de': 'NVIDIA A100 Tensor Core',
    'p3': 'NVIDIA Tesla V100',
    'p3dn': 'NVIDIA Tesla V100',
    'p2': 'NVIDIA K80',
    'g5': 'NVIDIA A10G Tensor Core',
    'g5g': 'NVIDIA T4G Tensor Core',
    'g4dn': 'NVIDIA T4 Tensor Core',
    'g4ad': 'AMD Radeon Pro V520',
    'g3': 'NVIDIA Tesla M60',
    'g3s': 'NVIDIA Tesla M60',
    'g2': '(Not listed)'
}

# Post filter here. 
for item in raw_data:
    item['cost'] = round(float(list(list(item['terms']['OnDemand'].items())[0][1]['priceDimensions'].items())[0][1]['pricePerUnit']['USD']), 3)
    item['cost_display'] = "{:.3f}".format(float(list(list(item['terms']['OnDemand'].items())[0][1]['priceDimensions'].items())[0][1]['pricePerUnit']['USD']), 3)
    item['name_key'] = item['product']['attributes']['instanceType'].split('.')[0]
    item['family'] = item['product']['attributes']['instanceFamily'].replace('Machine Learning', 'ML').replace('Instances', '')
    if item['name_key'] in gpu_names:
        item['gpu_name'] = gpu_names[item['name_key']]
        item['family_with_gpu'] = f"{item['product']['attributes']['instanceFamily']} {gpu_names[item['name_key']]}".replace('instance', '')
    else:
        item['gpu_name'] = ''
        item['family_with_gpu'] = f"{item['product']['attributes']['instanceFamily']}"
    if 'gpu' in item['product']['attributes']:
        item['gpu'] = item['product']['attributes']['gpu']
    else:
        item['gpu'] = '0'

    item['cpu'] = item['product']['attributes']['physicalProcessor']
    products.append(item)

gpu_table_rows = ''
for item in sorted(
    products, 
    key=lambda 
    x: (
        x['family_with_gpu'],
        x['product']['attributes']['instanceFamily'], 
        x['cost'], 
        x['product']['attributes']['instanceType'].split('.')[0],
        int(x['product']['attributes']['vcpu']),
        x['product']['attributes']['instanceType'])
    ):
    if item['gpu'] != '0': 
        gpu_table_rows += f"""
<tr>
<td class="family">{item['family_with_gpu'].replace('GPU ', '')}</td>
<td class="name_1">{item['product']['attributes']['instanceType'].split('.')[0]}</td>
<td class="name_2">{item['product']['attributes']['instanceType'].split('.')[1]}</td>
<td class="vcpu">{item['product']['attributes']['vcpu']}</td>
<td class="gpu">{item['gpu']}</td>
<td class="memory">{item['product']['attributes']['memory'].replace(' GiB', '')}</td>
<td class="cost">{item['cost_display']}</td>
<td class="cost">{item['cpu']}</td>
</tr>
"""


table_rows = ''
for item in sorted(
    products, 
    key=lambda 
    x: (
        x['product']['attributes']['instanceFamily'], 
        x['cost'], 
        x['product']['attributes']['instanceType'].split('.')[0],
        int(x['product']['attributes']['vcpu']),
        x['product']['attributes']['instanceType'])
    ):
    table_rows += f"""
<tr>
<td class="family">{item['family']}</td>
<td class="name_1">{item['product']['attributes']['instanceType'].split('.')[0]}</td>
<td class="name_2">{item['product']['attributes']['instanceType'].split('.')[1]}</td>
<td class="vcpu">{item['product']['attributes']['vcpu']}</td>
<td class="gpu">{item['gpu']}</td>
<td class="memory">{item['product']['attributes']['memory'].replace(' GiB', '')}</td>
<td class="cost">{item['cost_display']}</td>
<td class="gpu_name">{item['gpu_name']}</td>
<td class="gpu_name">{item['cpu']}</td>
</tr>
"""

with open('template.html') as _template:
    skeleton = Template(_template.read())
    with open('../../site/index.html', 'w') as _out:
        _out.write(skeleton.substitute(TABLE_ROWS=table_rows, GPU_TABLE_ROWS=gpu_table_rows))


