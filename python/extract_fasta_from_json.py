#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 09:49:52 2018

@author: jordanzehr
"""

import os

import json
import itertools as it
import argparse
from Bio.Seq import Seq


parser = argparse.ArgumentParser(
    description='Extract information from B-cell jsons.'
)
parser.add_argument(
    '-o', '--output',
    metavar='OUTPUT',
    type=str,
    help='Directory to output results',
    required=True
)
parser.add_argument(
    '-f', '--file',
    metavar='FILE',
    type=str,
    help='Name of JSON file to parse',
    required=True
)
parser.add_argument(
    '-s', '--size',
    metavar='SIZE',
    type=int,
    help='Discard entries whose size are below this threshold.',
    default=20
)

args = parser.parse_args()
input_path = args.file
size = args.size
output_directory = args.output

stem, extension = input_path.split('.')
filename = stem.split('/')[-1]
output_path_vars = (output_directory, filename, size)
output_path = '%s/%s_size-%d_unaligned.fasta' % output_path_vars
time = int(filename.split('_')[0])

with open(input_path, 'r') as input_file:
    data = json.load(input_file)

with open(output_path, 'w') as output_file:
    for i, item in enumerate(it.chain.from_iterable(data)):
        if int(item["size"]) > size:
            t = Seq(item["tag"]).split('|')[1]
            c = str(item["centroid"])[1:]
            j = str(item["tag"]).split(':')[0].split('|')[0]
            bad_t = []
            if '-' in t:
                bad_t.append(t)
            else:
                output_file.write(''.join(
                ['>seq' + str(i) + '_time-' + str(time) + '_size-' + str(item["size"]) + '_' 
                 + str((t).translate()[1:-2]) + '_' + str(j) + '_' + c.split(':')[10]]
            ))








