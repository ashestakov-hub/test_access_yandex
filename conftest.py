import json
import os

import pytest


@pytest.fixture(scope="function")
def test_case(request):
    test_name = request.node.name
    with open('test_cases/test_cases.json', 'r') as f:
        target_responses = json.load(f)
    yield target_responses['test_data'][test_name]

    try:
        os.remove("index.html")
    except OSError:
        pass
