#!/usr/bin/python 

from collections import deque
from Transaction import Transaction

class SimpleDatabase:

    def __init__(self):
        self._transStack = deque()
        self._values = dict()
        self._curTrans = None

    def begin(self):
        self._curTrans = Transaction()
        self._transStack.append( self._curTrans )

    def rollback(self):
        try:
            self._transStack.pop()
            return 0
        except IndexError:
            return "1"

    def commit(self):
        while (len(self._transStack) > 0):
            t = self._transStack.popleft()
            for var, val in t.getValues().iteritems():
                self._values[var] = val
            for var in t.getUnsetVars():
                del self._values[var]

    def set(self, var, value):
        pass

    def unset(self, var):
        pass

    def get(self, var):
        pass

    def numEqualTo(self, value):
        pass

    def getValues(self):
        pass

    def getUnset(self):
        pass

if __name__ ==  "__main__":
    db = SimpleDatabase()

    db.begin()
    db.begin()
    db.commit()
    db.commit()
    db.rollback()
    db.rollback()
    db.rollback()

    #t.set('a', '1')
    #t.set('b', '3')
    #t.set('c', '4')
    #t.set('d', '11')
    #t.set('e', '15')
    #t.unset('e')
    #t.unset('f')

    #for var, val in t.getValues().iteritems():
    #    print "{0} = {1}".format(var, val)

    #print "Variable e equal to {0}".format( t.get('e') )
    #print "Variable a equal to {0}".format( t.get('a') )
    #print "Variable d equal to {0}".format( t.get('d') )
    #print "Unset list: {0}".format( t.getUnset() )

    #print "Variable {0} are equal to 3".format( t.numEqualTo('3') )
    #print "Variable {0} are equal to 15".format( t.numEqualTo('15') )



