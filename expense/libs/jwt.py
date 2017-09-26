
def from_payload_to_user_info(payload):
    result = {}
    result['id'] = payload.get('user_id')
    result['username'] = payload.get("username")
    return result
