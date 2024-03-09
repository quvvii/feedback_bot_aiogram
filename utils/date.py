import datetime

def get_date() -> str:
    return datetime.datetime.now().strftime("%H:%M:%S, %d-%m-%Y")