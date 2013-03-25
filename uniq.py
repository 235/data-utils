#!/usr/bin/python
"""
    Similar as unix uniq, however does not require input steam to be sorted!
    Uses a probabalistic structure, therefore may rarely delete non-duplicated records
    (with the current settings its up to 0.1% in a sequence of 100'000'000 UNIQUE input rows)
"""
import os
import fileinput
from optparse import OptionParser
from pybloomfilter import BloomFilter

bloomfile = './_tmp_bloomfilter'
MAXUNIQUES = 100000000
ACCUACY = 0.001


def process(files):
    #Iterate over the lines of all files listed in sys.argv[1:], defaulting to sys.stdin if the list is empty.
    #If a filename is '-', it is also replaced by sys.stdin.
    if os.path.isfile(bloomfile):
        UNIQUES = BloomFilter.open(bloomfile)
    else:
        UNIQUES = BloomFilter(MAXUNIQUES, ACCUACY, bloomfile)

    for record in fileinput.input(files):
        record = str(record).strip()
        if not record in UNIQUES:
            UNIQUES.add(record)
            print record
    UNIQUES.sync()
    UNIQUES.close()

if __name__ == "__main__":
    """Read from stdin"""
    parser = OptionParser()
    # parser.add_option("-p", "--prefix", dest="prefix", default=None,
    #                   help="prefix for output files")
    # parser.add_option("-c", "--cnum", dest="cnum", default=None,
    #                   help="column number with GUID (starting 0)")

    (options, files) = parser.parse_args()
    process(files)
