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


class CohomologyError(CStarError):
    """
    Raised when the global topology prevents circuit generation.
    Analogue: LinkerError, RecursionError

    Example:
        The logic contains a paradox.
    """

    pass
