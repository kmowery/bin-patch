#!/usr/bin/env python

import argparse
import math
import sys
import re

parser = argparse.ArgumentParser(description="Make some plots.")
parser.add_argument('source')
parser.add_argument('-b', '--base', default='0',
    help="Location to start patch", metavar="addr")
parser.add_argument('-p', '--patch', default=argparse.SUPPRESS,
  help="Patch file", metavar="filename")
parser.add_argument('-o', '--output', required=True,
  help="Output location", metavar="filename")
args = vars(parser.parse_args())

patch_base = eval(args['base'])

blocksize = 1024

source = open(args['source'], 'r')
patch = open(args['patch'], 'r')
output = open(args['output'], 'w+')

patch.seek(0,2)
patch_size = patch.tell()

source.seek(0,2)
file_size = source.tell()

if file_size < patch_base + patch_size:
  print "Base + Patch size is larger than Source file. Aborting."
  ss.exit(1)

patch.seek(0)
source.seek(0)

written = 0

for i in range(patch_base / blocksize):
  buf = source.read(blocksize)
  if len(buf) != blocksize:
    print "something horrible has happened"
  output.write(buf)
  written += len(buf)

buf = source.read(patch_base-written)
output.write(buf)
written += len(buf)

print "source location: %d"%(source.tell())
while patch_size > 0:
  buf = patch.read(min(patch_size, blocksize))
  output.write(buf)
  source.seek(len(buf), 1)
  print "patching %d characters: %d"%( len(buf), source.tell())
  written += len(buf)
  patch_size -= len(buf)

while True:
  buf = source.read(blocksize)
  if len(buf) == 0:
    break
  output.write(buf)
  written += len(buf)

