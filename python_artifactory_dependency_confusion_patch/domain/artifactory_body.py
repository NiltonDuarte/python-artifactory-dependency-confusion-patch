from dataclasses import dataclass
from enum import Enum


class EventType(Enum):
    DEPLOYED = "DEPLOYED"


@dataclass
class DeployedData:
    repo_key: str
    path: str
    name: str
    sha256: str
    size: str


@dataclass
class ArtifactoryWebhookBodyContent:
    domain: str
    event_type: EventType
    subscription_key: str
    jpd_origin: str
    source: str
    data: dict

    def data_object(self):
        _map = {EventType.DEPLOYED: DeployedData}
        return _map[self.event_type](**self.data)

    @classmethod
    def load_from_dict(cls, content: dict):
        content = content.copy()
        try:
            content["event_type"] = EventType[content["event_type"].upper()]
        except Exception:
            raise RuntimeError(f"Event Type [{content['event_type'].upper()}] is not mapped")

        return cls(**content)
