from dataclasses import dataclass


@dataclass
class UploadResult:
    filename: str
    text: str
    error: str | None = None
