from exceptions import DateOrderError
from models import ParsedDeed


def validate_date_order(deed: ParsedDeed)->None:
    if deed.date_recorded <deed.date_signed:
        raise DateOrderError(
            deed.date_recorded.date(),deed.date_signed.date()
        )

