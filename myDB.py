import fileinput
import sys
from Parser import CommandParser
from Parser import ParseError
from SimpleDatabase import SimpleDatabase

def print_help():
    pass

if __name__ == "__main__":

    #print "Welcome to Mikhail's SimpleDatabase"
    #print_help()

    parser = CommandParser()
    db = SimpleDatabase()

    while 1:
        try:
            line = sys.stdin.readline()
            if not line:
                continue
            if len(line.strip()) == 0:
                continue
            cmd = parser.parse(line.strip())
            #print cmd.getType()
            if cmd.getType() == 'END':
                break
            ret = db.execute(cmd)
            if len(ret.strip()) > 0:
                print ret
        except KeyboardInterrupt:
            break
        except ParseError as e:
            print e
            continue
    
        #print line
