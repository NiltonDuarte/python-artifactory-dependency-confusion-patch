from python_artifactory_dependency_confusion_patch.pypi_service import PypiService, PypiConfig
import uuid


def test_check_exist():
    config = PypiConfig("https://test.pypi.org", "")
    # a very popular lib
    exists = PypiService(config).check_lib_exist("requests")
    assert exists

    # a lib that do not exist
    exists = PypiService(config).check_lib_exist(f"for_sure-a_lib-dont-exists-kekw-{uuid.uuid4()}")
    assert not exists
