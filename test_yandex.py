import pytest
from utils import command_handler, BrowserEmulator, execute_command, validate, validate_yandex_page, \
    validate_mail_page


@pytest.mark.functional
def test_access_with_browser(user_agent):
    browser = BrowserEmulator(user_agent)
    test_response = browser.open('https://yandex.ru')
    fs = browser.get_active_forms()
    assert validate_yandex_page(test_response, fs), "Yandex page wasn't open"


@pytest.mark.functional
def test_page_availability(availability_case):
    command_log = execute_command(availability_case["command"])
    assert validate(command_log, availability_case['expected_response']),\
        f"Unexpected {availability_case['command']} output please check logs"


@pytest.mark.functional
def test_certificated_access(certificate_case):
    command_log = command_handler(certificate_case["command"])
    assert validate(command_log, certificate_case['expected_response']),\
        f"Unexpected {certificate_case['command']} output please check logs"


@pytest.mark.functional
def test_login(user_agent, credentials):
    browser = BrowserEmulator(user_agent)
    browser.open("https://yandex.ru")
    browser.login(login=credentials["login"], password=credentials["passwd"])
    resp = browser.open('https://mail.yandex.ru/')
    assert validate_mail_page(resp), "Login wasn't successful"
