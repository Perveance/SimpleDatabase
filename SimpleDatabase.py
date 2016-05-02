from collections import deque
from Transaction import Transaction

class SimpleDatabase:

    def __init__(self):
        self._transQueue = deque()
        self._values = dict()
        self._curTrans = None

    def begin(self):
        t = Transaction()
        self._transQueue.append( t )
        self._curTrans = t

    def rollback(self):
        try:
            self._transQueue.pop()
            if len(self._transQueue) > 0:
                self._curTrans = self._transQueue[len(self._transQueue) - 1]
            return ""
        except IndexError:
            self._curTrans = None
            return "NO TRANSACTION"

    # This function will apply all current transactions to
    # get temporary results 
    def _trycommit(self, merged):
        for t in self._transQueue:
            for var, val in t.getValues().iteritems():
                merged[var] = val
            for var in t.getUnsetVars():
                try:
                    del merged[var]
                except:
                    pass

    # Commit each transaction in the transaction queue
    def doCommit(self, merged):
        while (len(self._transQueue) > 0):
            t = self._transQueue.popleft()
            for var, val in t.getValues().iteritems():
                merged[var] = val
            for var in t.getUnsetVars():
                del merged[var]

    def commit(self):
        if self._curTrans is None:
            return "NO TRANSACTION"
        self.doCommit(self._values)
        self._curTrans = None
        return ""

    def set(self, var, value):
        if self._curTrans:
            self._curTrans.set(var, value)
        else:
            self._values[var] = value

    def unset(self, var):
        if self._curTrans:
            self._curTrans.unset(var)
        else:
            try:
                del self._values[var]
            except KeyError:
                pass
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
    pass

