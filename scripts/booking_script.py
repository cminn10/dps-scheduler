import json
from datetime import datetime
import http.client
from config import *
import copy
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


########################

class DPSClient:
    def __init__(self):
        self.conn = http.client.HTTPSConnection("publicapi.txdpsscheduler.com")
        self.headers = {
            'Origin': 'https://public.txdpsscheduler.com',
            'Referer': 'https://public.txdpsscheduler.com/',
            'Content-Type': 'application/json;charset=UTF-8'
        }

    def request(self, path, payload, method="POST"):
        self.conn.request(method, path, json.dumps(payload), self.headers)
        res = self.conn.getresponse()
        if res.status == 200:
            data = res.read().decode("utf-8")
            return json.loads(data)
        elif res.status == 204:
            return None
        else:
            raise Exception(f"Request failed with status code {res.status}")


########################

target_date = datetime.strptime(LATEST_DATE, "%m/%d/%Y")
start_time = datetime.strptime(PREF_TIME['startTime'], "%H:%M")
end_time = datetime.strptime(PREF_TIME['endTime'], "%H:%M")

client = DPSClient()


def get_available_slots():
    location_payload = {
        "TypeId": TYPE_ID,
        "ZipCode": ZIP_CODE,
        "PreferredDay": 0
    }
    location_data = client.request("/api/AvailableLocation", location_payload)
    location_ids = []
    for i in location_data:
        curr_date = datetime.strptime(i['NextAvailableDate'], "%m/%d/%Y")
        if curr_date <= target_date:
            location_ids.append(i['Id'])
    available_slots = []
    for j in location_ids:
        schedule_payload = {
            "LocationId": j,
            "TypeId": TYPE_ID,
            "SameDay": False,
            "StartDate": None,
            "PreferredDay": 0
        }
        schedule_data = client.request("/api/AvailableLocationDates", schedule_payload)
        for k in schedule_data['LocationAvailabilityDates']:
            curr_date = datetime.strptime(k['AvailabilityDate'], "%Y-%m-%dT%H:%M:%S")
            if curr_date <= target_date and k['DayOfWeek'] in PREF_TIME['preferredDOW']:
                for h in k['AvailableTimeSlots']:
                    time = datetime.strptime(h['FormattedTime'], "%I:%M %p")
                    if start_time <= time <= end_time:
                        slot_info = {
                            "SlotId": h['SlotId'],
                            "BookingDateTime": h['StartDateTime'],
                            "SiteId": k['LocationId'],
                        }
                        available_slots.append(slot_info)
    return available_slots


def book_slots(available_slots):
    response_id = client.request("/api/Eligibility", LOGIN_INFO)[0]['ResponseId']
    hold_slot_payload = copy.deepcopy(LOGIN_INFO)
    success = False
    for slot in available_slots:
        hold_slot_payload['SlotId'] = slot['SlotId']
        body_text = ''
        hold_slot_res = client.request("/api/HoldSlot", hold_slot_payload)
        if hold_slot_res['SlotHeldSuccessfully']:
            body_text += f"Slot {slot['SlotId']}--{slot['BookingDateTime']} is successfully held.\n"
            booking_payload = {
                "CardNumber": "",
                "Email": EMAIL,
                "CellPhone": "",
                "HomePhone": "",
                "ServiceTypeId": 81,
                "BookingDateTime": slot['BookingDateTime'],
                "BookingDuration": 20,
                "SpanishLanguage": "N",
                "SiteId": slot['SiteId'],
                "SendSms": False,
                "AdaRequired": False,
                "ResponseId": response_id,
            }
            booking_payload = booking_payload | LOGIN_INFO
            booking_res = client.request("/api/NewBooking", booking_payload)
            if booking_res.get('Booking') is not None and booking_res.get('ErrorMessage') is None:
                confirmation_number = booking_res['Booking']['ConfirmationNumber']
                site_name = booking_res['Booking']['SiteName']
                site_address = booking_res['Booking']['SiteAddress']
                date_time = booking_res['Booking']['BookingDateTime']
                body_text += (f"Successfully booked at: {site_name}, {site_address}, {date_time}.\n"
                              f"Confirmation number: {confirmation_number}\n")
                client.request("/api/NewBooking", hold_slot_payload)
                body_text += f"Slot {slot['SlotId']}--{slot['BookingDateTime']} is released.\n"
                success = True
                break
            else:
                body_text += f"Slot {slot['SlotId']}--{slot['BookingDateTime']} is failed to book.\n"
                body_text += f"Error message: {booking_res.get('ErrorMessage')}\n"
            client.request("/api/NewBooking", hold_slot_payload)
            body_text += f"Slot {slot['SlotId']}--{slot['BookingDateTime']} is released.\n"
        else:
            body_text += f"Slot {slot['SlotId']}--{slot['BookingDateTime']} is failed to held.\n"
    return {
        "body_text": body_text,
        "success": success
    }


def send_email(body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = EMAIL
    msg['Subject'] = "Texas DPS Appointment Booking Result"
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
        smtp_server.starttls()
        smtp_server.login(SENDER_EMAIL, SENDER_PW)
        smtp_server.send_message(msg)
        print(f'Email sent: \n{body}')


def exec_booking():
    slots = get_available_slots()
    if len(slots) > 0:
        result = book_slots(slots)
        if SHOULD_SEND_EMAIL:
            send_email(result['body_text'])
        return result['success']
    return False


if __name__ == '__main__':
    exec_booking()
