from dataclasses import dataclass


@dataclass
class HealthStatus:
    status: str
    app: str
