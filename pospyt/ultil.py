from datetime import datetime

def convert_to_valid_format(date):
    if isinstance(date, datetime):
        # Use strftime to format Python datetime to the desired format
        formatted_datetime = date.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_datetime
    else:
        raise ValueError("Invalid input. Expected Python datetime object.")
     