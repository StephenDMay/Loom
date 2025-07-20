from typing import Any, Dict, List, Optional


class ContextManager:
    """
    Manages shared context and state across different agents in the system.
    
    This class provides a centralized repository for runtime data that can be
    accessed and modified by agents during execution. It uses a simple dictionary
    to store context data and provides methods to get, set, and update context.
    """

    def __init__(self):
        """Initialize the ContextManager with an empty context dictionary."""
        self._context: Dict[str, List[Any]] = {}

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get the most recent value from the context.

        Args:
            key (str): The key to retrieve the value for.
            default (Any): Default value to return if key doesn't exist.

        Returns:
            Any: The most recent value associated with the key, or default if key doesn't exist.
        """
        if key in self._context and self._context[key]:
            return self._context[key][-1]
        return default

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the context, replacing the entire history for the key.

        Args:
            key (str): The key to set the value for.
            value (Any): The value to set.
        """
        self._context[key] = [value]

    def add(self, key: str, value: Any) -> None:
        """
        Add a value to the context, accumulating it with previous values.

        Args:
            key (str): The key to add the value for.
            value (Any): The value to add.
        """
        if key not in self._context:
            self._context[key] = []
        self._context[key].append(value)

    def get_history(self, key: str) -> List[Any]:
        """
        Get the complete history of values for a key.

        Args:
            key (str): The key to retrieve the history for.

        Returns:
            List[Any]: The complete list of values for the key, or empty list if key doesn't exist.
        """
        return self._context.get(key, [])

    def update(self, data: Dict[str, Any]) -> None:
        """
        Update the context with multiple key-value pairs, replacing history for each key.

        Args:
            data (Dict[str, Any]): Dictionary of key-value pairs to update the context with.
        """
        for key, value in data.items():
            self.set(key, value)

    def clear(self) -> None:
        """Clear all context data."""
        self._context.clear()

    def keys(self):
        """Return the keys in the context."""
        return self._context.keys()

    def items(self):
        """Return the key-value pairs in the context (most recent values only)."""
        return {key: values[-1] if values else None for key, values in self._context.items()}.items()

    def __contains__(self, key: str) -> bool:
        """Check if a key exists in the context."""
        return key in self._context

    def __len__(self) -> int:
        """Return the number of items in the context."""
        return len(self._context)