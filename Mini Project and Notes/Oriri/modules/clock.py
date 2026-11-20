from datetime import datetime


def get_current_time(use_24_hour=False, show_seconds=False):
    now = datetime.now()

    if use_24_hour:
        time_format = "%H:%M:%S" if show_seconds else "%H:%M"
    else:
        time_format = "%I:%M:%S %p" if show_seconds else "%I:%M %p"

    return now.strftime(time_format).lstrip("0")


def get_current_date():
    return datetime.now().strftime("%A, %B %d, %Y")


def get_greeting():
    hour = datetime.now().hour

    if hour < 12:
        return "Good morning"
    elif hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"
