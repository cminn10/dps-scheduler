LATEST_DATE = '12/31/2023'
PREF_TIME = {
    "startTime": "12:30",
    "endTime": "17:00",
    "preferredDOW": [
        # "Monday",
        "Tuesday",
        # "Wednesday",
        "Thursday",
        "Friday"
    ]
}
EMAIL = "your email address"
LOGIN_INFO = {
    "FirstName": "John",
    "LastName": "Smith",
    "DateOfBirth": "01/01/1900",
    "LastFourDigitsSsn": "0000",
    # same as LastFourDigitsSsn
    "Last4Ssn": "0000"
}
ZIP_CODE = '11000'
TYPE_ID = 81  # for Change, replace or renew Texas DL/Permit

SHOULD_SEND_EMAIL = True
# SMTP Gmail sender
SENDER_EMAIL = 'your SMTP email sender address'
SENDER_PW = 'pw for SMTP email sender address'

# Job run settings
# Default: run every 2 minutes for 1 hour
RUN_DURATION = 60 * 60  # 1 hour
RUN_INTERVAL = 2 * 60  # 2 minutes
