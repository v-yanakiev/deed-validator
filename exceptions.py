class DeedValidationError(Exception):
    """Base for all deed validation failures."""

class DateOrderError(DeedValidationError):
    """Raised when a deed is recorded before it was signed."""

class AmountMismatchError(DeedValidationError):
    """Raised when the numeric amount disagrees with the written-word amount."""

class CountyNotFoundError(DeedValidationError):
    """Raised when we can't confidently match the county name."""
