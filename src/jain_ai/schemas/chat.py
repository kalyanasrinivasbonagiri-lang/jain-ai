from dataclasses import dataclass


@dataclass
class ChatTurn:
    role: str
    message: str
