#!/usr/bin/env python

import cv2      # opencv 3
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
    vids = filter(lambda x: x.lower().endswith('.avi') or x.lower().endswith('.mp4'), files)
    total += len(vids)

for root, dirs, files in os.walk(input_dir):
    vids = filter(lambda x: x.lower().endswith('.avi') or x.lower().endswith('.mp4'), files)
    vids = sorted(vids)
    for vid in vids:
        i += 1
        in_file = join(root, vid)
        out_file = in_file.replace(input_dir, output_dir, 1)
        out_file += '.npy'
        out_dir = os.path.dirname(out_file)
        print "(%d/%d) Saving to %s" % (i, total, out_file)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        cap = cv2.VideoCapture(in_file)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        ret, frame0 = cap.read()
        frame0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
        flows = np.zeros((frame_height, frame_width, (frame_count-1)*2), dtype='float32')
        
        idxFrame = 0
        while(cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            flows[...,idxFrame*2:idxFrame*2+2] = cv2.calcOpticalFlowFarneback(frame0, frame, None, 0.5, 3, 4, 3, 5, 1.1, 0)

            #if flows is None:
            #    flows = flow
            #else:
            #    flows = np.concatenate((flows,flow), axis=2)

            frame0 = frame
            idxFrame += 1

        idxFrame += 1 # because of the first frame we dropped
        if idxFrame != frame_count:
            print('warning: Frame size read is different from the actual frame size for file "' + in_file + '"\nread: %d, actual: %d' % (frame_count, idxFrame))
            flows = flows[...,:(idxFrame-1)*2]

        cap.release()
        np.save(out_file, flows)




