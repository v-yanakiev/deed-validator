from modules.exceptions import AmountMismatchError, DateOrderError
from modules.models import ParsedDeed
from word2number import w2n

def validate_date_order(deed: ParsedDeed)->None:
    if deed.date_recorded <deed.date_signed:
        raise DateOrderError(
            deed.date_recorded.date(),deed.date_signed.date()
        )

def validate_amount_consistency(deed: ParsedDeed, tolerance: float = 0.01) -> None:
    try:
        amount_from_words = float(_words_to_number(deed.amount_words))
    except ValueError:
        raise ValueError(f"Failed to convert {deed.amount_words} to number!")
    
    if abs(deed.amount_numeric - amount_from_words) > tolerance:
        raise AmountMismatchError(deed.amount_numeric, deed.amount_words, amount_from_words)
    
def _words_to_number(words: str) -> float:
    return float(w2n.word_to_num(words))  # type: ignore[reportUnknownMemberType]
