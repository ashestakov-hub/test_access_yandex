import os
import pytest
import subprocess
import pexpect
from utils import grep, Logger
import mechanize


@pytest.mark.functional
def test_atc1_1():
    url = 'https://yandex.ru'
    br = mechanize.Browser()

    # set up the browser configuration
    br.set_handle_equiv(False)
    br.set_handle_robots(False)
    br.addheaders = [('User-agent',
                      'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) '
                      'Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    # open Yandex main page
    resp = br.open(url)

    # basically Yandex page has 2 forms: login to mail and search
    fs = br.forms()
    assert 2 == len(fs)
    assert 'https://passport.yandex.ru/passport?mode=auth&retpath=https://mail.yandex.ru/' == fs[0].action
    assert 'https://yandex.ru/search/' == fs[1].action
    test_response = resp.read().decode('utf-8')

    # Check page content
    assert 'content="https://yandex.ru"' == grep('content="https:\/\/yandex\.ru"', test_response)
    assert 'method="POST" action="https://passport.yandex.ru/passport?mode=auth&retpath=https://mail.yandex.ru/"' == grep('method="POST" action="https:\/\/passport\.yandex\.ru\/passport\?mode=auth&retpath=https:\/\/mail\.yandex\.ru\/"', test_response)
    assert 'action="https://yandex.ru/search/" role="search"' == grep('action="https:\/\/yandex.ru\/search\/" role="search"', test_response)


@pytest.mark.functional
def test_atc1_2(test_case):
    ping_response = subprocess.Popen([r"ping -c 6 yandex.ru"], shell=True,
                                     stdout=subprocess.PIPE).communicate()[0].strip().decode('utf-8')
    "4 packets transmitted, 4 packets received, 0.0% packet loss"
    result = grep("\d packets transmitted, \d received, \d{1,3}% packet loss", ping_response)
    assert test_case['expected_response'] == result


@pytest.mark.functional
def test_atc1_3(test_case):
    curl_response = subprocess.Popen([r"curl -Is https://yandex.ru | head -1"], shell=True,
                                     stdout=subprocess.PIPE).communicate()[0].strip().decode('utf-8')
    assert test_case['expected_response'] == curl_response


@pytest.mark.functional
def test_atc1_4(test_case):
    logger = Logger()
    ssl = pexpect.spawn("openssl s_client -connect yandex.ru:443", logfile=logger)
    ssl.sendline("HEAD / HTTP/1.1")
    ssl.sendline("HOST: yandex.ru")
    ssl.send('\n')
    ssl.send('\n')
    ssl.expect_exact("X-Yandex-Sdch-Disable: 1")
    ssl.sendcontrol('c')
    ssl.expect(pexpect.EOF)
    ssl.terminate()
    result = grep("HTTP/\d.\d \d\d\d", logger.log)
    assert test_case['expected_response'] == result


@pytest.mark.functional
def test_atc1_5():
    subprocess.Popen(["wget yandex.ru 443"], shell=True,
                     stdout=subprocess.PIPE).communicate()[0].strip().decode('utf-8')

    assert os.path.isfile("index.html")


@pytest.mark.functional
def test_atc1_6(test_case):
    logger = Logger()
    ssl = pexpect.spawn("nc yandex.ru 443", logfile=logger)
    ssl.sendline("HEAD / HTTP/1.1")
    ssl.sendline("HOST: yandex.ru")
    ssl.send('\n')
    ssl.send('\n')
    ssl.expect_exact("X-Yandex-Sdch-Disable: 1")
    ssl.sendcontrol('c')
    ssl.expect(pexpect.EOF)
    ssl.terminate()
    result = grep("HTTP/\d.\d \d\d\d", logger.log)
    assert test_case['expected_response'] == result


@pytest.mark.functional
def test_atc2_1(test_case):
    url = 'https://yandex.ru'
    br = mechanize.Browser()

    # set up the browser configuration
    br.set_handle_equiv(False)
    br.set_handle_robots(False)
    br.addheaders = [('User-agent',
                      'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) '
                      'Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    # open Yandex main page
    br.open(url)
    br.select_form(nr=0)

    #  logging in
    br.form['login'] = test_case['login']
    br.form['passwd'] = test_case['passwd']
    br.submit()

    # once login, the brwoser stores cookie data which allow us to open for example authorized Yandex.Mail page
    resp = br.open('https://mail.yandex.ru/')
    test_response = resp.read().decode('utf-8')

    # Check special for authorised page fields and titles
    assert 'xmlns:mail="urn:yandex:mail"' == grep('xmlns:mail="urn:yandex:mail"', test_response)
    assert '<title>Inbox' == grep('<title>Inbox', test_response)
    assert 'Yandex.Mail' == grep('Yandex.Mail', test_response)
    assert 'action="mailbox.check"' == grep('action="mailbox.check"', test_response)
    assert 'href="https://yandex.ru"><img border="0" alt="Yandex"' == grep(r'href="https://yandex.ru"><img border="0" alt="Yandex"', test_response)
