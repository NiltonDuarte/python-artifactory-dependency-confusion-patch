import logging
import sys
from pathlib import Path
import json
import pytest
from dotenv import load_dotenv

resource_folder = Path(__file__).parent / "resources"

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)


def pytest_addoption(parser):
    parser.addoption("--run-e2e", action="store_true", default=False, help="run e2e tests")


def pytest_configure(config):
    config.addinivalue_line("markers", "e2e: mark test as e2e run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-e2e"):
        return
    skip_e2e = pytest.mark.skip(reason="need --run-e2e option to run")
    for item in items:
        if "e2e" in item.keywords:
            item.add_marker(skip_e2e)


@pytest.fixture
def sample_input_dict():
    sample_input_path = resource_folder / "sample_input.json"
    with open(str(sample_input_path), "r") as f:
        content = f.read()
        sample_dict = json.loads(content)
    return sample_dict


@pytest.fixture
def load_test_dotenv():
    load_dotenv(resource_folder / ".env")
