#!/usr/bin/python 

class Transaction:

    def __init__(self):
        self._values = dict()
        self._unsetList = []

    def set(self, var, value):
        self._values[var] = value

    def unset(self, var):
        self._unsetList.append(var)
        print self._unsetList
        try:
            del self._values[var]
        except KeyError:
            pass

    def get(self, var):
        try:
            return self._values[var]
        except KeyError:
            return None

    def numEqualTo(self, value):
        count = 0
        for var, val in self._values.iteritems():
            if val == value:
                count += 1
        return count

    def getValues(self):
        return self._values

    def getUnsetVars(self):
        return self._unsetList

if __name__ ==  "__main__":
    t = Transaction()

    t.set('a', '1')
    t.set('b', '3')
    t.set('c', '4')
    t.set('d', '11')
    t.set('e', '15')
    t.unset('e')
    t.unset('f')

    for var, val in t.getValues().iteritems():
        print "{0} = {1}".format(var, val)

    print "Variable e equal to {0}".format( t.get('e') )
    print "Variable a equal to {0}".format( t.get('a') )
    print "Variable d equal to {0}".format( t.get('d') )
    print "Unset list: {0}".format( t.getUnsetVars() )

    print "Variable {0} are equal to 3".format( t.numEqualTo('3') )
    print "Variable {0} are equal to 15".format( t.numEqualTo('15') )

