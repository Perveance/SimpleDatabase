#

class Command:

    def __init__(self, cmdType, arg1=None, arg2=None):
        #print "Command created"
        self._type = cmdType
        self._args = []
        if arg1: 
            self._args.append(arg1)
        if arg2: 
            self._args.append(arg2)

    def getType(self):
        return self._type
    def getArgs(self):
        return self._args

class ParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
       return repr(self.value)

class CommandParser:

    def __init__(self):
        #print "Parser created"
        pass

    def parse(self, line):

        words = line.split()
        if len(words) == 0:
            raise PraseError("Empty input")

        if words[0] == 'END':
            return Command('END')
        elif words[0] == 'BEGIN':
            return Command('BEGIN')
        elif words[0] == 'ROLLBACK':
            return Command('ROLLBACK')
        elif words[0] == 'COMMIT':
            return Command('COMMIT')
        elif words[0] == 'SET':
            if len(words) != 3:
                raise ParseError("SET command needs 2 arguments")
            return Command('SET', words[1], words[2])
        elif words[0] == 'GET':
            if len(words) != 2:
                raise ParseError("GET command needs 1 arguments")
            return Command('GET', words[1])
        elif words[0] == 'UNSET':
            if len(words) != 2:
                raise ParseError("UNSET command needs 1 arguments")
            return Command('UNSET', words[1])
        elif words[0] == 'NUMEQUALTO':
            if len(words) != 2:
                raise ParseError("NUMEQUALTO command needs 1 arguments")
            return Command('NUMEQUALTO', words[1])
        else:
             raise ParseError('Unrecognized Command')


