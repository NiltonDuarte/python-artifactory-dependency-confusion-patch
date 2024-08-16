import os
import pytest
import uuid
from python_artifactory_dependency_confusion_patch import reserve_pypi_name_from_artifactory
from python_artifactory_dependency_confusion_patch import NotificationService, SlackNotification
from python_artifactory_dependency_confusion_patch import PublicNameReserver
from python_artifactory_dependency_confusion_patch.notification_service import NoOpNotification


@pytest.mark.e2e
def test_run_e2e(sample_input_dict, load_test_dotenv):
    sample_input_dict["data"]["path"] = f"lib-name-{uuid.uuid4()}"
    reserve_pypi_name_from_artifactory(sample_input_dict)


@pytest.mark.e2e
def test_run_e2e__notification_system(sample_input_dict, load_test_dotenv):
    slack_webhook = os.environ.get("SLACK_WEBHOOK")
    if slack_webhook:
        notification = SlackNotification(slack_webhook)
    else:
        notification = NoOpNotification()
    notification_service = NotificationService(notification)

    name_reserver = PublicNameReserver(notification_service)
    sample_input_dict["data"]["path"] = "requests"
    name_reserver.reserve_name_from_artifactory_body(sample_input_dict)
