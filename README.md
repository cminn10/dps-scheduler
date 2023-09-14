# Texas DPS Scheduler

## Usage
Make sure you have Python 3.6 or higher installed. Then, run the following commands:
Start the job:
```bash
# Clone the repository
cd ./scripts
# update config.py with your information
python3 main.py
```
Or run the booking script directly once:
```bash
python3 booking_script.py
```

## Configuration
The configuration file is located at `./scripts/config.py`. Please update the settings per your requirements.

### Config fields explained
`LATEST_DATE` - The latest date you want to book an appointment for. The script will book the earliest available appointment before this date.

`PREF_TIME.startTime/endTime` - The earliest/latest time of the day you want to book an appointment for.

`EMAIL` - The email address you will to receive confirmation emails from the DPS.

`TYPE_ID` - The type of appointment you want to book. Refer to [TYPE_ID mapping](#type-mapping) for more information.

`SHOULD_SEND_EMAIL` - Whether you want to receive confirmation emails from the **script**.
If yes, you need to have a valid Gmail account with:
* SMTP enabled
* An [app password](https://support.google.com/accounts/answer/185833?hl=en) generated, and update the `SENDER_EMAIL` and `SENDER_PW` fields.

`RUN_DURATION` - The duration of the script in seconds. The script will stop running after this duration.

`RUN_INTERVAL` - The interval between each run in seconds.

### Cron job
Texas DPS usually releases new appointments around 7:00 AM CST on weekdays. You can set up a daily cron job to run the script at 7:00 AM CST using crontab:
`0 7 * * 1-5 cd /path/to/scripts && python3 main.py`


## <a id='type-mapping'></a> TYPE_ID mapping
| Type ID | Category                           | Appointment Type                                 |
|---------|------------------------------------|--------------------------------------------------|
| 21      | Road Skills Tests                  | Class C                                          |
| 51      | Road Skills Tests                  | RV                                               |
| 61      | Road Skills Tests                  | Public Safety                                    |
| 73      | Commercial Driver License Services | Apply for first time Texas CLP/CDL               |
| 78      | Commercial Driver License Services | Apply/Renew Non-Domicile CDL                     |
| 81      | Driver License Services            | Change, replace or renew Texas DL/Permit         |
| 85      | Driver License Services            | Returning to take a computer or written test     |
| 86      | Driver License Services            | Driver License Address Change                    |
| 87      | Other Services                     | I received a correction no fee letter from DPS   |
| 91      | Other Services                     | Schedule a home-bound visit                      |
| 101     | Other Services                     | Lawful Presence Verification Complete            |
| 121     | Road Skills Tests                  | Non-CDL Class A/Class B                          |
| 710     | Other Services                     | Service not listed or my license is not eligible |
| 901     | Other Services                     | I am required to take a road test                |

