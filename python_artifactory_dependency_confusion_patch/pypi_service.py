import os
from functools import cache
from dataclasses import dataclass
from pathlib import Path
import requests
from build.__main__ import main as build_project
from twine import cli as upload_cli


class SecretStr:
    def __init__(self, secret):
        self._secret = secret

    def get_secret(self):
        return self._secret

    def __str__(self):
        return "SecretStr(*****)"

    def __repr__(self):
        return self.__str__()


class PypiException(Exception):
    def __init__(self, response: requests.Response) -> None:
        message = f"Unexpected response from PyPi [{response.status_code}]: {response.text}"
        super().__init__(message)


@dataclass
class PypiConfig:
    repository_url: str
    token: SecretStr

    def __post_init__(self):
        if not isinstance(self.token, SecretStr):
            self.token = SecretStr(self.token)

    @classmethod
    def load_from_env(cls):
        return cls(repository_url=os.environ["PYPICONFIG_ENDPOINT"], token=os.environ["PYPICONFIG_TOKEN"])


class PypiService:
    # https://test.pypi.org/project/requests/
    pypi_lookup_template = "{repository}/project/{lib_name}/"

    def __init__(self, config: PypiConfig) -> None:
        self.config = config

    @classmethod
    def from_config_env(cls):
        return PypiService(PypiConfig.load_from_env())

    @cache
    def check_lib_exist(self, lib_name) -> True:
        response = requests.get(
            self.pypi_lookup_template.format(repository=self.config.repository_url, lib_name=lib_name)
        )
        if response.status_code == 200:
            return True
        if response.status_code == 404:
            return False
        # something unexpected happened
        raise PypiException(response)

    def ship_lib(self, lib_path: Path | str):
        build_project([f"{lib_path}"])

        upload_cli.dispatch(
            [
                "upload",
                f"{lib_path}/dist/*",
                "--username",
                "__token__",
                "--password",
                self.config.token.get_secret(),
                "--repository-url",
                f"{self.config.repository_url}/legacy/",
                "--non-interactive",
                # "--skip-existing",
                "--verbose",
                "--disable-progress-bar",
            ]
        )
