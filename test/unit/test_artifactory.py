from python_artifactory_dependency_confusion_patch.domain.artifactory_body import ArtifactoryWebhookBodyContent
from python_artifactory_dependency_confusion_patch.artifactory_service import ArtifactoryService


def test_load_class(sample_input_dict):
    content = ArtifactoryWebhookBodyContent.load_from_dict(sample_input_dict)
    assert content.domain == "artifact"


def test_load_data_class(sample_input_dict):
    content = ArtifactoryWebhookBodyContent.load_from_dict(sample_input_dict)
    data_content = content.data_object()
    assert data_content.sha256 == "1318b7b4fe17d431377ee8a3b0264c9fc0f8483c9563de7bf9aead45cea0ba44"


def test_artifactory_service(sample_input_dict):
    lib_name = ArtifactoryService.from_content(sample_input_dict).lib_name()
    assert lib_name == "lib-name"
