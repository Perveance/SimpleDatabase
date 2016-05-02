
class Transaction:

    def __init__(self):
        self._values = dict()
        self._unsetList = []

    def set(self, var, value):
        self._values[var] = value

    def unset(self, var):
        self._unsetList.append(var)
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
    pass

