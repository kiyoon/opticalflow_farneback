#!/usr/bin/env python

import sys
import numpy as np
import os
from os.path import join

if len(sys.argv) < 3:
    print "usage: %s [input_dir] [output_dir]" % sys.argv[0]
    print "Author: Kiyoon Kim (yoonkr33@gmail.com)"
    sys.exit()

input_dir = sys.argv[1]
output_dir = sys.argv[2]
if input_dir.endswith('/'):
    input_dir = input_dir[:-1]
if output_dir.endswith('/'):
    output_dir = output_dir[:-1]

i = 0
total = 0
for root, dirs, files in os.walk(input_dir):
    npys = filter(lambda x: x.lower().endswith('.npy'), files)
    total += len(npys)

for root, dirs, files in os.walk(input_dir):
    npys = filter(lambda x: x.lower().endswith('.npy'), files)
    npys = sorted(npys)
    for npy in npys:
        i += 1
        in_file = join(root, npy)
        out_file = in_file.replace(input_dir, output_dir, 1)
        out_dir = os.path.dirname(out_file)
        out_file = out_file[:-4]        # remove extension (.npy)
        print "(%d/%d) Processing %s" % (i, total, in_file)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        flows = np.load(in_file)
        for j in range(flows.shape[2] // 2 - 19):
            np.save("%s_%06d.npy" % (out_file, j), flows[...,j*2:j*2+20])




