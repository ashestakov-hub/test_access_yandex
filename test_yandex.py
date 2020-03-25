import pytest
from utils import grep, command_handler, BrowserEmulator, execute_command, validate


@pytest.mark.functional
def test_access_with_browser(user_agent):
    browser = BrowserEmulator(user_agent)
    test_response = browser.open('https://yandex.ru')
    fs = browser.get_active_forms()
    assert 2 == len(fs)
    assert 'https://passport.yandex.ru/passport?mode=auth&retpath=https://mail.yandex.ru/' == fs[0].action
    assert 'https://yandex.ru/search/' == fs[1].action
    # Check page content
    assert 'content="https://yandex.ru"' == grep('content="https:\/\/yandex\.ru"', test_response), "Couldn't find expected page contenct"
    assert 'method="POST" action="https://passport.yandex.ru/passport?mode=auth&retpath=https://mail.yandex.ru/"' == grep(
        'method="POST" action="https:\/\/passport\.yandex\.ru\/passport\?mode=auth&retpath=https:\/\/mail\.yandex\.ru\/"',
        test_response), "Couldn't find authentication form on page"
    assert 'action="https://yandex.ru/search/" role="search"' == grep(
        'action="https:\/\/yandex.ru\/search\/" role="search"', test_response), "Couldn't find Search form on page"


@pytest.mark.functional
def test_page_availability(availability_case):
    command_log = execute_command(availability_case["command"])
    assert validate(command_log, availability_case['expected_response']), f"Unexpected {availability_case['command']} output please check logs"


@pytest.mark.functional
def test_certificated_access(certificate_case):
    command_log = command_handler(certificate_case["command"])
    assert validate(command_log, certificate_case['expected_response']),  f"Unexpected {certificate_case['command']} output please check logs"


@pytest.mark.functional
def test_atc2_1(user_agent, credentials):
    browser = BrowserEmulator(user_agent)
    browser.open("https://yandex.ru")
    browser.login(login=credentials["login"], password=credentials["passwd"])
    resp = browser.open('https://mail.yandex.ru/')
    test_response = resp
    assert 'xmlns:mail="urn:yandex:mail"' != grep('xmlns:mail="urn:yandex:mail"', test_response), "Couldn't find expected element on Mail page. Login wasn't successfull"
    assert '<title>Inbox' == grep('<title>Inbox', test_response), "Couldn't find expected element on Mail page. Login wasn't successfull"
    assert 'Yandex.Mail' == grep('Yandex.Mail', test_response), "Couldn't find expected element on Mail page. Login wasn't successfull"
    assert 'action="mailbox.check"' == grep('action="mailbox.check"', test_response), "Couldn't find expected element on Mail page. Login wasn't successfull"
    assert 'href="https://yandex.ru"><img border="0" alt="Yandex"' == grep(
        r'href="https://yandex.ru"><img border="0" alt="Yandex"', test_response), "Couldn't find expected element on Mail page. Login wasn't successfull"
