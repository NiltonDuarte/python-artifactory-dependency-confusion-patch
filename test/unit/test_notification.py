from python_artifactory_dependency_confusion_patch.notification_service import NotificationService
from python_artifactory_dependency_confusion_patch.pypi_service import PypiLookupResponse


class KeepLastNotification:
    def __init__(self) -> None:
        self.last_message = None

    def notify(self, message):
        self.last_message = message


known_email = {"known_email"}
suppress_email = {"suppress_email"}


def test_notification_system__unknown_email():
    response = PypiLookupResponse("lib_name", True, "unknown_email")
    keep_last_notification = KeepLastNotification()
    assert keep_last_notification.last_message is None
    notification_service = NotificationService(keep_last_notification, known_email, suppress_email)
    notification_service.notify(response)
    assert keep_last_notification.last_message is not None


def test_notification_system__known_email():
    response = PypiLookupResponse("lib_name", True, "known_email")
    keep_last_notification = KeepLastNotification()
    assert keep_last_notification.last_message is None
    notification_service = NotificationService(keep_last_notification, known_email, suppress_email)
    notification_service.notify(response)
    assert keep_last_notification.last_message is None


def test_notification_system__suppressed_email():
    response = PypiLookupResponse("lib_name", True, "suppress_email")
    keep_last_notification = KeepLastNotification()
    assert keep_last_notification.last_message is None
    notification_service = NotificationService(keep_last_notification, known_email, suppress_email)
    notification_service.notify(response)
    assert keep_last_notification.last_message is None
