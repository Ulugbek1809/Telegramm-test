import datetime


def hozirgi_vaqt():
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
