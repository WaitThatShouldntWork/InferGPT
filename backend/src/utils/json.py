import json


def to_json(input, error_message="Failed to interpret JSON"):
    try:
        return json.loads(input)
    except Exception:
        raise Exception(f'{error_message}: "{input}"')
