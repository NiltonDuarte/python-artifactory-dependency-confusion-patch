import logging

from python_artifactory_dependency_confusion_patch.artifactory_service import ArtifactoryService
from python_artifactory_dependency_confusion_patch.lib_generator import LibGenerator
from python_artifactory_dependency_confusion_patch.pypi_service import PypiService
from python_artifactory_dependency_confusion_patch.notification_service import NotificationService

logger = logging.getLogger(__name__)


class PublicNameReserver:
    def __init__(self, notification_service: NotificationService) -> None:
        self.notification_service = notification_service

    def reserve_name_from_artifactory_body(self, artifactory_body):
        lib_name = ArtifactoryService.from_content(artifactory_body=artifactory_body).lib_name()
        pypi_service = PypiService.from_config_env()
        pypi_response = pypi_service.check_lib_exist(lib_name)
        if pypi_response.found:
            logging.debug(f"Lib [{lib_name}] already exists. Sending to NotificationService")
            self.notification_service.notify(pypi_response)
            return

        lib_gen = LibGenerator.from_lib_name(lib_name)
        lib_path = lib_gen.create_lib_structure()
        pypi_service.ship_lib(lib_path)
        lib_gen.delete_lib_structure(lib_path)
