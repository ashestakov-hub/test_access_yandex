import json
import re
import subprocess

import mechanize
import pexpect


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


def command_handler(command):
    logger = Logger()
    ssl = pexpect.spawn(command, logfile=logger)
    ssl.sendline("HEAD / HTTP/1.1")
    ssl.sendline("HOST: yandex.ru")
    ssl.send('\n')
    ssl.send('\n')
    ssl.expect_exact("X-Yandex-Sdch-Disable: 1")
    ssl.sendcontrol('c')
    ssl.expect(pexpect.EOF)
    ssl.terminate()
    write_logs(command, logger.log)
    return logger.log


def validate(log, expected_string):
    log = log.split('\n')
    if expected_string in log:
        return True
    else:
        return False


def adopt_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def execute_command(command):
    log = subprocess.Popen([command], shell=True,
                           stdout=subprocess.PIPE).communicate()[0].strip().decode('utf-8')
    write_logs(command, log)
    return log


def write_logs(command, log):
    name = command.replace(" ", "_").replace("|", "").replace("/", "_")
    with open(f"tmp/logs/{name}.log", "w") as log_file:
        log_file.write(log)


class BrowserEmulator(object):
    def __init__(self, user_agent):
        self.br = mechanize.Browser()
        self.br.set_handle_equiv(False)
        self.br.set_handle_robots(False)
        self.br.addheaders = [('User-agent', user_agent)]
        self.resp = None

    def open(self, url):
        return self.br.open(url).read().decode('utf-8')

    def get_active_forms(self):
        return self.br.forms()

    def login(self, login, password):
        self.br.select_form(nr=0)
        self.br.form['passwd'] = password
        self.br.form['login'] = login
        self.br.submit()
