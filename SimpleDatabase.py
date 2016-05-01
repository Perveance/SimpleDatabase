from collections import deque
from Transaction import Transaction

class SimpleDatabase:

    def __init__(self):
        self._transStack = deque()
        self._values = dict()
        self._curTrans = None

    def begin(self):
        #print " --> Begin ENTER: length of transaction stack is {0}".format(len(self._transStack))
        t = Transaction()
        self._transStack.append( t )
        #print " --> Begin EXIT: length of transaction stack is {0}".format(len(self._transStack))
        self._curTrans = t

    def rollback(self):
        try:
            #print " --> Rollback ENTER: length of transaction stack is {0}".format(len(self._transStack))
            self._transStack.pop()
            #print " --> Rollback 2: length of transaction stack is {0}".format(len(self._transStack))
            if len(self._transStack) > 0:
                self._curTrans = self._transStack[len(self._transStack) - 1]
            #print " --> Rollback EXIT 0: length of transaction stack is {0}: {1}".format(len(self._transStack), self._transStack[0].getValues())
            #print " --> Rollback EXIT 0: values: {0}".format(self._values)
            return ""
        except IndexError:
            self._curTrans = None
            #print " --> Rollback EXIT 1: length of transaction stack is {0}".format(len(self._transStack))
            return "NO TRANSACTION"

    def _trycommit(self, merged):
        for t in self._transStack:
            for var, val in t.getValues().iteritems():
                merged[var] = val
            for var in t.getUnsetVars():
                try:
                    del merged[var]
                except:
                    pass



    def _commit(self, merged):
        while (len(self._transStack) > 0):
            t = self._transStack.popleft()
            for var, val in t.getValues().iteritems():
                merged[var] = val
            for var in t.getUnsetVars():
                del merged[var]

    def commit(self):
        if self._curTrans is None:
            return "NO TRANSACTION"
        self._commit(self._values)
        self._curTrans = None
        return ""

    def set(self, var, value):
        #print "set: Enter self._curTrans = {0}".format(self._curTrans)
        if self._curTrans:
            #print "set: in curTrans"
            self._curTrans.set(var, value)
        else:
            #print "set: in values"
            self._values[var] = value

    def unset(self, var):
        #print "  -> unset Enter"
        if self._curTrans: # TODO: should we go through every transaction?
            #print "  -> unset current transaction"
            self._curTrans.unset(var)
        else:
            try:
                del self._values[var]
            except KeyError:
                pass
        #print "  -> unset Exit"
        return ""


    def get(self, var):

        ret = None
        if self._curTrans:
            tmpValues = dict(self._values)
            self._trycommit(tmpValues)
            try:
                ret = tmpValues[var]
            except:
                ret = "NULL"
        else:
            try:
                ret = self._values[var]
            except KeyError:
                ret = "NULL"
        return ret

    def numEqualTo(self, value):
        tmpRes = dict(self._values)
        count = 0;
        self._trycommit(tmpRes)
        for var, val in tmpRes.iteritems():
            if val == value:
                count += 1
        return str(count)

    def execute(self, cmd):
        ret = ""
        if cmd.getType() == 'BEGIN':
            self.begin()
        elif cmd.getType() == 'ROLLBACK':
            ret = self.rollback()
        elif cmd.getType() == 'COMMIT':
            ret = self.commit()
        elif cmd.getType() == 'SET':
            self.set(cmd.getArgs()[0], cmd.getArgs()[1])
        elif cmd.getType() == 'GET':
            ret = self.get(cmd.getArgs()[0])
        elif cmd.getType() == 'UNSET':
            ret = self.unset(cmd.getArgs()[0])
        elif cmd.getType() == 'NUMEQUALTO':
            ret = self.numEqualTo(cmd.getArgs()[0])
        else:
            ret = "Unknown command"
        return ret
        

if __name__ ==  "__main__":

    db = SimpleDatabase()

    print " <<< values 1 = {0}".format(db._values)
    db.set('b', '25')
    print " <<< values 2 = {0}".format(db._values)
    db.begin()
    print " --> After Begin: length of transaction stack is {0}".format(len(db._transStack))
    print " <<< values 3 = {0}".format(db._values)
    db.set('a', '10')

    print " --> After Set: length of transaction stack is {0}".format(len(db._transStack))
    print " <<< values 4 = {0}".format(db._values)


    print "a = {0}".format(db.get('a'))
    print " --> After Get: length of transaction stack is {0}".format(len(db._transStack))
    print "b = {0}".format(db.get('b'))
    print " --> Before begin: length of transaction stack is {0}".format(len(db._transStack))
    db.begin()
    #print " <<< values before set = {0}".format(db._values)
    db.set('a', '20')

    #print " <<< values before get = {0}".format(db._values)

    #print "second get a = {0}".format( db.get('a') )
    #print " <<< values after get = {0}".format(db._values)
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

