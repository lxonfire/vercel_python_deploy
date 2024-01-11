from flask import Flask, request, jsonify
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

app = Flask(__name__)

def format_number(input_number):
    return phonenumbers.parse(f"+{input_number}", None)

@app.route('/', methods=['GET'])
def scan_number():
    number = request.args.get('number')

    if not number:
        return jsonify({'error': 'Phone number is required'}), 400

    phone_number_object = format_number(number)

    if not phonenumbers.is_valid_number(phone_number_object):
        return jsonify({'error': 'Invalid phone number'}), 400

    number_info = {
        'developer': 'lxbadboy.t.me',
        'international_format': phonenumbers.format_number(phone_number_object, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
        'local_format': phonenumbers.format_number(phone_number_object, phonenumbers.PhoneNumberFormat.E164),
        'country': geocoder.country_name_for_number(phone_number_object, "en"),
        'location': geocoder.description_for_number(phone_number_object, "en"),
        'carrier': carrier.name_for_number(phone_number_object, "en"),
        'timezones': [str(tz) for tz in timezone.time_zones_for_number(phone_number_object)],
        'is_possible': phonenumbers.is_possible_number(phone_number_object)
    }

    return jsonify(number_info)

if __name__ == '__main__':
    app.run()
