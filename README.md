bin-patch
=========

This is an extremely simple binary patching tool. Given file A, file B, and
offset N, create file C which is A with B overlaid at position N.

Example
-------
File source_file:

    0123456789

File patch_file:

    FFFF

Run:

    $ patch.py source_file -p patch_file -b 2 -o output.txt

output.txt will contain:

    01FFFF6789


