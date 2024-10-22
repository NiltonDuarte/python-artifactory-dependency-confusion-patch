# Python Artifactory Dependency Confusion Patch

This application is designed to work in conjunction with the Artifactory webhook to reserve names in the python public repository. When new python libraries are deployed to the internal Artifactory repository the webhook notifies the application and the name is reserved if available.

## Python Dependency Confusion Supply Chain Attack

Supply chain attack vectors are becoming increasingly popular. This issue gained widespread attention through the blog post [Dependency Confusion: How I Hacked Into Apple, Microsoft and Dozens of Other Companies](https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610). The Python environment is particularly vulnerable to such attacks.

If not configured properly, the Python dependency manager protocol can be exploited to install a malicious package instead of the intended one. The most common misconfiguration involves adding a private repository to the tool and allowing it to decide which version/package to download between the public and private repositories. By default, it will choose the package with the higher version number.

An attacker can exploit this by deploying a known library from a private repository into the public repository with a very high version number (e.g., version 999.9.9), thereby confusing the tool into installing the malicious package.

## Artifactory

[JFROG Artifactory](https://jfrog.com/artifactory/) is a popular private artifact repository that can also serve as a private repository for Python libraries. Artifactory includes built-in [features](https://jfrog.com/blog/addressing-the-npm-manifest-confusion-vulnerability/) to help mitigate dependency confusion attacks. However, it cannot fully solve the problem if the dependency management tool is not configured correctly.

## Patching

The strategy of this application is to *reserve the name on the public repository* to prevent it from being taken by a malicious actor and used as an attack vector. If the name is already taken, it can optionally send a notification to a Slack webhook.

The application leverages the Artifactory [webhook](https://jfrog.com/help/r/jfrog-platform-administration-documentation/predefined-webhooks) for `deployed` events to reserve the name.

Name reservation is done by publish a useless library with the same name into the python public repository with version `0.0.0`

The package is meant to be used on an application that receives the Artifactory webhook `POST` request and send the JSON content to the library, as in the usage example.

### Flowchart

![flowchart](./docs/static/flowchart.png)

### Usage Example

Usage example [code](./docs/cloud_function_example.py) ([requirements.txt](./docs/gcf_requirements.txt)) in a google cloud function:

```python
import functions_framework
import traceback
import logging
from python_artifactory_dependency_confusion_patch import NotificationService, SlackNotification
from python_artifactory_dependency_confusion_patch import PublicNameReserver

logger = logging.getLogger("python_artifactory_dependency_confusion_patch")

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

```

Note: `"fix deps <fix@python.deps>"` is the author email from the template

Note: For testing set `TWINE_REPOSITORY_URL` to test repository