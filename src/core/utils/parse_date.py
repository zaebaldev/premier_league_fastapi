from datetime import date, datetime


def parse_date(str_date: str) -> date:
    for str_date_fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y", "%d-%m-%Y", "%d-%m-%y"):
        try:
            return datetime.strptime(str_date, str_date_fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {str_date}")
