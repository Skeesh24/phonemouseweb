from abc import ABC, abstractmethod


class IBroker(ABC):
    @abstractmethod
    def __init__(self, host: str, port: int, queue: str):
        pass

    @abstractmethod
    def open(self):
        """Open a connection to the broker."""
        pass

    @abstractmethod
    def close(self):
        """Close a connection to the broker."""
        pass

    @abstractmethod
    def send(self, body: str):
        """Send a message to the broker."""
        pass

    @abstractmethod
    def receive(self) -> str:
        """Receive a message from the broker."""
        pass
