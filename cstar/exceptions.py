class CStarError(Exception):
    """Base class for all C* language errors."""

    pass


class ObstructionError(CStarError):
    """
    Raised when a specific definition violates physical laws.
    Analogue: TypeError, ValueError

    Example:
        Context('Bad', [X, Z])  # Doesn't commute
    """

    pass
