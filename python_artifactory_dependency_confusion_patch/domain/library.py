from dataclasses import dataclass


@dataclass
class Library:
    name: str
    namespace: str = None

    def __post_init__(self):
        if self.namespace is None:
            self.namespace = self.name.replace("-", "_")
