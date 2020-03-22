import re


class Logger(object):
    def __init__(self):
        self.log = ''

    def write(self, *args):
        for line in args:
            self.log += line.decode('utf-8').replace("\r", "")

    def flush(self):
        pass


def grep(pattern="", log=''):
    m = re.search('({})'.format(pattern), log, re.U)
    try:
        return m.group(0)
    except AttributeError:
        return ''
