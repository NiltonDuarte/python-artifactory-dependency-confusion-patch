from python_artifactory_dependency_confusion_patch.pypi_service import PypiService, PypiConfig, _local_cache
import uuid


def test_check_exist():
    config = PypiConfig("https://test.pypi.org", "")
    # a very popular lib
    pypi_response = PypiService(config).check_lib_exist("requests")
    assert pypi_response.found
    assert "requests" in _local_cache

    # a lib that do not exist
    pypi_response = PypiService(config).check_lib_exist(f"for_sure-a_lib-dont-exists-kekw-{uuid.uuid4()}")
    assert not pypi_response.found
