import sys
import requests
import traceback

CRASHBIN_URL = 'http://crashbin.example.org/api/report/new/'

def handle_exception(exc_type, exc_value, exc_traceback):
    title = traceback.format_exception_only(exc_type, exc_value)[0]
    text = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    requests.post(CRASHBIN_URL, {'title': title, 'log': text})
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

sys.excepthook = handle_exception

def main():
    raise Exception("Unhandled exception")

main()
