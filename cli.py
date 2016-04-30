#!/usr/bin/python

import fileinput
import sys
from Parser import CommandParser
from Parser import ParseError

def print_help():
    pass

if __name__ == "__main__":

    print "Welcome to MKH Database"
    print_help()

    parser = CommandParser()
    #db = SimpleDatabase()

    while 1:
        try:
            line = sys.stdin.readline()
            if not line:
                continue
            if len(line.strip()) == 0:
                continue
            cmd = parser.parse(line.strip())
            print cmd.getType()
            #ret = db.execute(cmd)
            #print ret
        except KeyboardInterrupt:
            break
        except ParseError as e:
            print e
            continue
    
        print line
