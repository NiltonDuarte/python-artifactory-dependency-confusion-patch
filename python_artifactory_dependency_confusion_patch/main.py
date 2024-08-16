import logging

from python_artifactory_dependency_confusion_patch.artifactory_service import ArtifactoryService
from python_artifactory_dependency_confusion_patch.lib_generator import LibGenerator
from python_artifactory_dependency_confusion_patch.pypi_service import PypiService

logger = logging.getLogger(__name__)


def reserve_pypi_name_from_artifactory(webhook_body_json: dict):
    lib_name = ArtifactoryService.from_content(artifactory_body=webhook_body_json).lib_name()
    pypi_service = PypiService.from_config_env()
    if pypi_service.check_lib_exist(lib_name).found:
        logging.debug(f"Lib [{lib_name}] already exists. Exiting")
        return

    lib_gen = LibGenerator.from_lib_name(lib_name)
    lib_path = lib_gen.create_lib_structure()
    pypi_service.ship_lib(lib_path)
    lib_gen.delete_lib_structure(lib_path)
