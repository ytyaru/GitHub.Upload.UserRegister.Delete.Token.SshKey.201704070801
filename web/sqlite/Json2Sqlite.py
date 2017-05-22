#!python3
#encoding:utf-8
class Json2Sqlite(object):
    def __init__(self):
        pass

    def BoolToInt(self, bool_value):
        if True == bool_value:
            return 1
        else:
            return 0
    def IntToBool(self, int_value):
        if 0 == int_value:
            return False
        else:
            return True

    def ArrayToString(self, array):
        if None is array or 0 == len(array):
            return None
        ret = ""
        for v in array:
            ret += v + ','
            print(ret)
        print(ret[:-1])
        return ret[:-1]
    def StringToArray(self, string):
        if None is string or 0 == len(string):
            return None
        array = []
        for item in string.sprit(','):
            if 0 < len(item):
                array.append(item)
        return array
