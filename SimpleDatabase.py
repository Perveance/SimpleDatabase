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
            self._curTrans = self._transStack[len(self._transStack) - 1]
            return 0
        except IndexError:
            return "1"

    def _commit(self, merged):
        while (len(self._transStack) > 0):
            t = self._transStack.popleft()
            for var, val in t.getValues().iteritems():
                merged[var] = val
            for var in t.getUnsetVars():
                del merged[var]

    def commit(self):
        self._commit(self._values)
        self._curTrans = None

    def set(self, var, value):
        if self._curTrans:
            self._curTrans.set(var, value)
        else:
            self._values[var] = value

    def unset(self, var):
        print "  -> unset Enter"
        if self._curTrans:
            print "  -> unset current transaction"
            self._curTrans.unset(var)
        else:
            try:
                del self._values[var]
            except KeyError:
                pass
        print "  -> unset Exit"


    def get(self, var):

        ret = None
        if self._curTrans:
            tmpValues = dict(self._values)
            self._commit(tmpValues)
            try:
                ret = tmpValues[var]
            except:
                ret = None
        else:
            try:
                ret = self._values[var]
            except KeyError:
                ret = None
        return ret

    def numEqualTo(self, value):
        tmpRes = dict(self._values)
        count = 0;
        self._commit(tmpRes)
        for var, val in tmpRes.iteritems():
            if val == value:
                count += 1
        return count

if __name__ ==  "__main__":

    db = SimpleDatabase()

    db.set('b', '25')
    db.begin()
    db.set('a', '10')
    print "a = {0}".format(db.get('a'))
    print "b = {0}".format(db.get('b'))
    db.begin()
    db.set('a', '20')
    print "second get a = {0}".format( db.get('a') )
    print "b = {0}".format(db.get('b'))
    db.rollback()
    print "After rollback a should be 10. a = {0}".format(db.get('a'))
    print "should be 25 b = {0}".format(db.get('b'))
    db.commit()
    print "a = {0}".format(db.get('a'))
    print "b = {0}".format(db.get('b'))
    db.rollback() # This doesn't do anything
    db.set('a', '30') # Not in transaction
    db.set('b', '10')
    print "(should be 30) a = {0}".format(db.get('a'))
    print "(should be 10) b = {0}".format(db.get('b'))
    #print "numequalto 10 = {0}".format(db.numEqualTo('10'))
    db.begin() 
    db.unset('a')
    print "after unset should be none a = {0}".format(db.get('a'))
    print "b = {0}".format(db.get('b'))
    db.rollback()
    print "should be 30 a = {0}".format(db.get('a'))
    db.unset('a')
    print "a = {0}".format(db.get('a'))
    print "b = {0}".format(db.get('b'))
    print "numequalto 10 = {0}".format(db.numEqualTo('10'))

