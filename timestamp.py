#!/usr/bin/python
"""
    Parses unix timestamp column and replaces with custom data format
"""
import sys
import fileinput
from optparse import OptionParser
import datetime


def process(files, cnum, delimiter):
    #Iterate over the lines of all files listed in sys.argv[1:], defaulting to sys.stdin if the list is empty.
    #If a filename is '-', it is also replaced by sys.stdin.

    for record in fileinput.input(files):
        record = str(record).strip().split(delimiter)
        try:
            print delimiter.join(record[:cnum] +
                                 [datetime.datetime.fromtimestamp(int(record[cnum])).strftime('%Y-%m-%d %H:%M:%S'), ] +
                                 record[cnum + 1:])
        except:
            print >> sys.stderr, 'Wrong timeformat in line: %s' % record

if __name__ == "__main__":
    """Read from stdin"""
    parser = OptionParser()
    parser.add_option("-c", "--cnum", dest="cnum", default=1,
                      help="column number with user_agent (starting 1)")
    parser.add_option("-d", "--delimiter",  dest="delimiter", default="\t",
                      help="Column delimiter",
                      metavar="delimiter")

    (options, files) = parser.parse_args()
    process(files, int(options.cnum) - 1, options.delimiter)
