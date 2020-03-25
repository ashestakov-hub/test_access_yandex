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


def validate_yandex_page(test_response, fs):
    forms = 2 == len(fs)
    mail_form = 'https://passport.yandex.ru/passport?mode=auth&retpath=https://mail.yandex.ru/' == fs[0].action
    search_form = 'https://yandex.ru/search/' == fs[1].action
    # Check page content
    content = 'content="https://yandex.ru"' == grep('content="https:\/\/yandex\.ru"', test_response)
    mail_html = 'method="POST" action="https://passport.yandex.ru/passport?mode=auth&retpath=https://mail.yandex.ru/"' == grep(
        'method="POST" action="https:\/\/passport\.yandex\.ru\/passport\?mode=auth&retpath=https:\/\/mail\.yandex\.ru\/"',
        test_response)
    search_html= 'action="https://yandex.ru/search/" role="search"' == grep(
        'action="https:\/\/yandex.ru\/search\/" role="search"', test_response)
    if forms and mail_form and search_form and content and mail_form and mail_html and search_html:
        return True
    else:
        return False


def validate_mail_page(test_response):
    mail = 'xmlns:mail="urn:yandex:mail"' == grep('xmlns:mail="urn:yandex:mail"',
                                                  test_response)
    inbox = '<title>Inbox' == grep('<title>Inbox',
                                  test_response)
    title = 'Yandex.Mail' == grep('Yandex.Mail',
                                 test_response)
    action = 'action="mailbox.check"' == grep('action="mailbox.check"',
                                            test_response)
    href = 'href="https://yandex.ru"><img border="0" alt="Yandex"' == grep(
        r'href="https://yandex.ru"><img border="0" alt="Yandex"',
        test_response)

    if mail and inbox and title and action and href:
        return True
    else:
        return False


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
