import json
import os

import pytest
from utils import adopt_json


@pytest.fixture(scope="session", autouse=True)
def prepare():
    try:
        os.makedirs("tmp/logs/")
    except OSError:
        pass


@pytest.fixture(scope="function")
def credentials():
    with open('test_cases/credentials.json', 'r') as f:
        return json.load(f)


def pytest_generate_tests(metafunc):
    if 'user_agent' in metafunc.fixturenames:
        ua = adopt_json('test_cases/user_agents.json')
        metafunc.parametrize("user_agent", ua)

    if 'availability_case' in metafunc.fixturenames:
        pa = adopt_json('test_cases/test_page_availability.json')
        metafunc.parametrize("availability_case", pa)

    if 'certificate_case' in metafunc.fixturenames:
        cc = adopt_json('test_cases/test_certificated_access.json')
        metafunc.parametrize("certificate_case", cc)
