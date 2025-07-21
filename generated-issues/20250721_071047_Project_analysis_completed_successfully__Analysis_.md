# EXTRACTED OUTPUT

Loaded cached credentials.
    def __str__(self) -> str:
        """Return a string representation of the current context state."""
        return str({key: values[-1] if values else None for key, values in self._context.items()})