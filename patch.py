#!/usr/bin/env python

import argparse
import itertools
import math
import sys
import re

parser = argparse.ArgumentParser(description="Make some plots.")
parser.add_argument('source')
parser.add_argument('-b', '--base', default='0',
    help="Location to start patch", metavar="addr")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-p', '--patch', default=argparse.SUPPRESS,
  help="Patch file", metavar="filename")
group.add_argument('-x', '--hexpatch', default=argparse.SUPPRESS,
    help="Patch content in hex", metavar="HEX_NUMBER")
parser.add_argument('-o', '--output', required=True,
  help="Output location", metavar="filename")

args = vars(parser.parse_args())

patch_base = eval(args['base'])

blocksize = 1024

source = open(args['source'], 'r')

if 'patch' in args:
  patch = open(args['patch'], 'r')
  patch.seek(0,2)
  patch_size = patch.tell()
elif 'hexpatch' in args:
  hexpatch = args['hexpatch']
  if len(hexpatch) % 2 != 0:
    print "Hexidecimal patch must be an integer number of bytes. Aborting."
    sys.exit(1)
  patch_size = len(hexpatch)/2
else:
  print "Unknown patch type. Shouldn't get here!"

source.seek(0,2)
file_size = source.tell()

if file_size < patch_base + patch_size:
  print "Base + Patch size is larger than Source file. Aborting."
  sys.exit(1)

output = open(args['output'], 'w+')
if 'patch' in args:
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

print "Patching at: 0x%x"%(source.tell())
while patch_size > 0:
  if 'patch' in args:
    buf = patch.read(min(patch_size, blocksize))
    output.write(buf)
    source.seek(len(buf), 1)
    print "patching %d characters: %d"%( len(buf), source.tell())
    written += len(buf)
    patch_size -= len(buf)
  elif 'hexpatch' in args:
    buf = hexpatch[:blocksize*2]
    hexpatch = hexpatch[len(buf):]
    patch_size = len(hexpatch)/2

    bytes = [chr(int(a+b, 16)) for a,b in
        itertools.izip(itertools.islice(buf, 0, None, 2),
                       itertools.islice(buf, 1, None, 2))]
    output.write("".join(bytes))

  else:
    print "Unknown patch type. Shouldn't get here!"

while True:
  buf = source.read(blocksize)
  if len(buf) == 0:
    break
  output.write(buf)
  written += len(buf)

