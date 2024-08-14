from python_artifactory_dependency_confusion_patch.domain.artifactory_body import (
    ArtifactoryWebhookBodyContent,
    EventType,
    DeployedData,
)


class ArtifactoryService:
    def __init__(self, artifactory_content: ArtifactoryWebhookBodyContent) -> None:
        self.artifactory_content = artifactory_content

    @classmethod
    def from_content(cls, artifactory_body: dict) -> "ArtifactoryService":
        artifactory_content = ArtifactoryWebhookBodyContent.load_from_dict(artifactory_body)
        return cls(artifactory_content)

    def lib_name(self) -> str:
        if self.artifactory_content.event_type == EventType.DEPLOYED:
            deployed_data: DeployedData = self.artifactory_content.data_object()
            lib_name = deployed_data.path.split("/")[0]
        return lib_name
