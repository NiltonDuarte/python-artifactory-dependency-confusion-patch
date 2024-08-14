import pytest
import uuid
from python_artifactory_dependency_confusion_patch.main import reserve_pypi_name_from_artifactory


@pytest.mark.e2e
def test_run_e2e(sample_input_dict, load_test_dotenv):
    sample_input_dict["data"]["path"] = f"lib-name-{uuid.uuid4()}"
    reserve_pypi_name_from_artifactory(sample_input_dict)
