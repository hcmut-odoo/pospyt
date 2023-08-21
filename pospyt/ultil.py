from datetime import datetime
import copy

from .constant import DATE_FORMAT_FULL, DATE_FORMAT_PARTIAL

def _try_convert_str_to_datetime(str_datetime):
    try:
        # check if str_datetime is partian format -> convert to datetime
        datetime_partial = datetime.strptime(str_datetime, DATE_FORMAT_PARTIAL)
        return datetime_partial
    except ValueError:
        # check if str_datetime is full format -> convert to datetime
        try:
            datetime_full = datetime.strptime(str_datetime, DATE_FORMAT_FULL)
            return datetime_full
        except ValueError:
            # by default, return datetime at current timepstap
            current_datetime = datetime.now()
            return current_datetime
                
def convert_to_valid_format(date):
    modified_date = copy.deepcopy(date)

    # Use strftime to format Python datetime to the desired format
    if isinstance(modified_date, datetime):
        formatted_datetime = modified_date.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_datetime

    elif isinstance(modified_date, str):
        modified_date_to_datetime = _try_convert_str_to_datetime(modified_date)
        formatted_datetime = modified_date_to_datetime.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_datetime

    else:
        raise ValueError("Invalid input. Expected Python datetime object.")
     