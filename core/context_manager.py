from typing import Any, Dict, Optional


class ContextManager:
    """
    Manages shared context and state across different agents in the system.
    
    This class provides a centralized repository for runtime data that can be
    accessed and modified by agents during execution. It uses a simple dictionary
    to store context data and provides methods to get, set, and update context.
    """

    def __init__(self):
        """Initialize the ContextManager with an empty context dictionary."""
        self._context: Dict[str, Any] = {}

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the context.

        Args:
            key (str): The key to retrieve the value for.
            default (Any): Default value to return if key doesn't exist.

        Returns:
            Any: The value associated with the key, or default if key doesn't exist.
        """
        return self._context.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the context.

        Args:
            key (str): The key to set the value for.
            value (Any): The value to set.
        """
        self._context[key] = value

    def update(self, data: Dict[str, Any]) -> None:
        """
        Update the context with multiple key-value pairs.

        Args:
            data (Dict[str, Any]): Dictionary of key-value pairs to update the context with.
        """
        self._context.update(data)

    def clear(self) -> None:
        """Clear all context data."""
        self._context.clear()

    def keys(self):
        """Return the keys in the context."""
        return self._context.keys()

    def items(self):
        """Return the key-value pairs in the context."""
        return self._context.items()

    def __contains__(self, key: str) -> bool:
        """Check if a key exists in the context."""
        return key in self._context

    def __len__(self) -> int:
        """Return the number of items in the context."""
        return len(self._context)