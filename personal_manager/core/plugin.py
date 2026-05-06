from abc import ABC, abstractmethod

class Plugin(ABC):
    """
    Base class for all plugins in the Personal Manager.
    All plugins must implement the name, description, and run methods.
    """
    @property
    @abstractmethod
    def name(self) -> str:
        """The display name of the plugin."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """A brief description of what the plugin does."""
        pass

    @abstractmethod
    def run(self) -> None:
        """The main execution logic of the plugin."""
        pass
