import functions_framework
from hashlib import sha256
import traceback
import logging
from python_artifactory_dependency_confusion_patch import NotificationService, SlackNotification
from python_artifactory_dependency_confusion_patch import PublicNameReserver

logger = logging.getLogger("test-python-supply-chain-attack")

notification_system = SlackNotification("<slack url>")
notification_service = NotificationService(notification_system, known_emails={"fix deps <fix@python.deps>"})
name_reserver = PublicNameReserver(notification_service)


@functions_framework.http
def reserve_name(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    try:
        name_reserver.reserve_name_from_artifactory_body(request_json)
    except Exception as exc:
        print(f"Failed to process request {request_json}")
        print(traceback.format_exc())

    return ("", 200)
