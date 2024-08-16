import logging
from typing import Optional, Protocol
import requests
from python_artifactory_dependency_confusion_patch.pypi_service import PypiLookupResponse

logger = logging.getLogger(__name__)


class NotificationSystem(Protocol):
    def notify(message): ...


class NoOpNotification:
    def notify(message): ...


class SlackNotification:
    def __init__(self, slack_webhook) -> None:
        self.slack_webhook = slack_webhook

    def notify(self, message):
        content = {"text": message}
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.slack_webhook, json=content, headers=headers)
        if response.status_code >= 400:
            logger.error(f"Failed to notify: [{message}]")


class NotificationService:
    def __init__(
        self,
        notification_system: NotificationSystem,
        known_emails: Optional[set] = None,
        suppress_emails: Optional[set] = None,
    ) -> None:
        self.known_emails = known_emails or set()
        self.suppress_emails = suppress_emails or set()
        self.notification_system = notification_system

    def notify(self, pypi_response: PypiLookupResponse):
        if pypi_response.author_email in self.known_emails:
            # no need to notify for know emails
            return
        message = f"Lib found in the public index: [lib={pypi_response.lib_name}] [author={pypi_response.author_email}]"
        if pypi_response.author_email in self.suppress_emails:
            # do not notify in suppress, only log
            logger.info(message)
            return
        self.notification_system.notify(message)
