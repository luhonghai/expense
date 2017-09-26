import phonenumbers

AFRICA_COUNTRY_CODE = "ZA"

def validate_phone_number(phone_string):
    check_phone = phonenumbers.parse(phone_string, region=AFRICA_COUNTRY_CODE)
    validate_data = {
        "is_valid": False,
        "phone_number": phone_string
    }
    if phonenumbers.is_valid_number(check_phone):
        validate_data["is_valid"] = True
        validate_data["phone_number"] = str(check_phone.national_number)
    return validate_data
