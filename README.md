bin-patch
=========

This is an extremely simple binary patching tool. Given file A, file B, and
offset N, create file C which is A with B overlaid at position N.

Note that all numbers should be given in hexadecimal.

Example
-------
With the sample files:

    $ echo 0123456789 > source_file
    $ echo FFFF > patch_file

Run:

    $ patch.py source_file -p patch_file --base 2 -o output.txt

output.txt will contain:

    01FFFF6789

You could also pass in the patch in hex:

    $ patch.py source_file -x FFFF --base 2 -o output.txt

